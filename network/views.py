from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# This will let me use json.loads() to convert JSON into a Python object (source:
# https://docs.python.org/3/library/json.html)
import json

# This will let me send and receive JSON data (source: my "mail" homework assignment)
from django.http import JsonResponse

# This adds the "CSRF exempt" function (source: my "mail" homework assignment)
from django.views.decorators.csrf import csrf_exempt

# This adds the pagination functionality (source: https://docs.djangoproject.com/en/4.0/topics/pagination/ .)
from django.core.paginator import Paginator

# This Imports all the models
from .models import User, Post, Follower, Like

""" This will let me use the "@login_required" attribute (source: my "commerce"
homework submmission: 
https://github.com/me50/eduardoluis11/tree/web50/projects/2020/x/commerce )
"""
from django.contrib.auth.decorators import login_required

# This will let me import the forms from forms.py
from .forms import CreatePostForm

# This will let me take the current date and time for the timestamp
import datetime

""" Index view. This will have the "All Posts" page.

Here, I will call the post creation Django form from forms.py. 

Now, I need to insert the post into the database. I will do that via the index() view. I will use an “if” to check if 
the user has clicked on the “submit” button. If they have, I will execute the Query Set statements needed to insert 
the data from the form into the database. 

The data that I need to insert into the database are all of the columns for the Post table. I will first get the data 
from the inputs from the post creation form. Then, I will need the ID of the logged user. The timestamp will be 
obtained by calling the datetime.datetime.now() function. I will set the number of likes to 0 by default.

Then, I will use a Query Set query to prepare the data to insert it into the database. 

I will make a query to the database to get all of the posts so that I can display them on the "All Posts" page. 
That should be done via a Query Set, and by using the all() function. The problem is that I need to arrange them
so that the most recent ones are shown first (reverse chronological order). I might need to add a filter.

To order by ascending or descending order according to a specific column in Query Set, I need to use the “order_by” 
attribute, and add a negative sign if I want the reverse of the default order (source: Keith’s reply on  
https://stackoverflow.com/questions/9834038/django-order-by-query-set-ascending-and-descending  .) I also need to add 
the name of the column between quotation marks. 
 
I will call here the custom pagination function that only 10 posts appear in the "All Posts" page.

What I tried to do didn’t work. I will try doing something else that I saw on the Paginator documentation. I will first 
go to one of the two views in which I will need to paginate the views. Then, I will call the Paginator() call on the 
variable that stores all of the posts. Then, I will store the page number in a variable that has the following code: 
    request.GET.get('page')

Next, I will create yes another variable, I which I will call the page number. To do that, I will insert the following 
snippet inside of the new variable:
    paginated_variable.get_page(page_number)

Finally, in the return() function of the view(), I will send the variable via Jinja notation.

Source of the code from the previous 3 paragraphs: https://docs.djangoproject.com/en/4.0/topics/pagination/ 

It seems that I need to add the page number as a 2nd parameter in “request.GET.get()” so that I enter into that 
page, and so it doesn’t print me “None” in the console (source: https://testdriven.io/blog/django-pagination/ .) 

Fixed it: it turns out that I was putting the Jinja code in the return() function of the index() view that is only 
activated AFTER creating a new post. I should have put the Jinja variable in the return(render) function that renders 
all the posts in the database. Reading this example repo helped me fix a bug to make my posts show up via Jinja after 
using the paginator: https://github.com/testdrivenio/django-pagination-example .

BUG: Whenever I post a post, all posts disappear. They only reappear when I go back to the home page. 

BUG FIX: I just needed to add the Jinja variable that stored the paginated posts in the "if" statement that
creates a new post.

I may add Jinja notation to check if the logged user is the author of that post, and if so, I will show an “edit” link 
on that post. However, this may be error prone. So, ideally, I should check if the logged user is the author of that 
post in the views. But remember: I should add those conditions to both the index() and the profile() views. If that 
condition is met, I’ll create a boolean variable, and I’ll set it to “True” to render the “Edit” link.
	
Then, I’ll send that boolean to the home and profile pages via Jinja. If the Boolean that checks if the logged user is 
the author of that post is “True”, I will render the “Edit” link. I will only decide whether to change that Boolean if 
the user’s logged in. So, I will have to add a “login” decorator to the condition that asks me if the logged user is the 
author of a specific post.

To check if a user is logged in within a view’s code, I need to use this code snippet (source: my “commerce” homework 
assignment):    
    if request.user.is_authenticated:
    
After further consideration, I think that it’s just much easier to use Jinja notation to check if the author of a post 
is the logged user using only Jinja notation directly on the HTML files. Jinja stores the name of the logged user in 
the “user.username” variable.

"""
def index(request):

    # This gets all the posts from the database
    all_posts = Post.objects.all().order_by('-timestamp')

    # This will store a Boolean that tells me whether to render the "Edit" link on a post
    render_edit_link = False

    # This will paginate the posts so that each page has 10 posts
    paginated_posts = Paginator(all_posts, 10)

    # DEBUG msg: this prints the object that was created when I first called the Paginator class
    print(paginated_posts)

    # This gets the current paginated page
    # Prints "None" if I don't specify a page, or "1" if I add "1" as a parameter
    current_page_number = request.GET.get('page', 1)

    # DEBUG msg
    print(current_page_number)

    # This gets all the posts of the current page
    # Prints "<Page 1 of 2>"
    paginated_posts_in_current_page = paginated_posts.get_page(current_page_number)

    # DEBUG msg
    print(paginated_posts_in_current_page)

    # Debug msg: this the total number of posts
    print(paginated_posts.count)    # Prints 11

    # DEBUG msg: This prints how many pages are in total after paginating
    print(paginated_posts.num_pages)    # Prints 2

    # DEBUG msg: This will print all posts, and the page to which those posts belong to
    for i in paginated_posts.page_range:
        print(paginated_posts.page(i))  # Prints page number
        print(paginated_posts.page(i).object_list)  # Prints posts in that page in a generic object format

        # This prints each post
        for post in paginated_posts.page(i).object_list:
            print(post.body)

    # This calls the post creation form
    form = CreatePostForm()

    # This declares a variable that will store the user's username as a string
    logged_user_string = ''

    # This checks if the user is logged in. If they do, I will send the user's username as a string in Jinja
    if request.user.is_authenticated:
        logged_user_string = str(request.user)


    # This checks if the "submit" button has been clicked
    if request.method == "POST":
        new_post = request.POST["new_post"]

        logged_user = request.user  # This gets the data from the logged user
        logged_user_id = logged_user.id  # ID of the user

        # This gets an instance of the logged user
        user_instance = User.objects.get(id=logged_user_id)

        current_timestamp = datetime.datetime.now()

        # This prepares the data before inserting it into the database
        new_post_created = Post(user=user_instance, body=new_post, number_of_likes=0, timestamp=current_timestamp)

        # This inserts the data into the database
        new_post_created.save()

        # Confirmation flash message
        post_creation_success_message = 'Your post has been created!'

        # This reloads the page and shows the confirmation message
        return render(request, "network/index.html", {
            "form": form,
            "post_creation_success_message": post_creation_success_message,
            "all_posts": all_posts,
            "paginated_posts_in_current_page": paginated_posts_in_current_page,
            "logged_user_string": logged_user_string,
        })

    # I'll try to paginate the posts by calling my paginate function here
    return render(request, "network/index.html", {
        "form": form,
        "all_posts": all_posts,
        "paginated_posts_in_current_page": paginated_posts_in_current_page,
        "logged_user_string": logged_user_string,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

""" Profile page view.

Since the profile page will change depending on the user that logs in, I need a parameter. I WON’T add the “login 
required” decorator since even people who aren’t logged in should be able to see any person’s profile page. So, what 
I’ll do is to take the username from the post or from the navbar, and I’ll insert it as a parameter in the profile() 
view. That way, I’ll know which profile page to render.

To check if a user exists before sending them into the user’s profile page, I will use the following snippet from my 
submission from the “mail” homework assignment (source: 
https://github.com/me50/eduardoluis11/tree/web50/projects/2020/x/mail .)
        try:
            user_variable = User.objects.get(username=username_from_parameter)
        except User.DoesNotExist:
    		return render(request, "network/profile.html", {
        		"error_message": "That username does not exist."
    		})

If the error message is not empty, I will add a conditional that prevents the title of the page from being rendered.

Writing “{% url profile %}” in the href of the usernames in the posts won’t work. If I do that, I will simply go to 
profile.html, but without obtaining the username of the post that I just clicked, so I will see buggy behavior. So, 
I will have to put a link like “profile/{{username_from_post}}” in the href of the <a> tag that will contain the 
post’s username.

I still haven’t implemented the “following” functionality. So, all users will have 0 followers.

To display the followers on the profile page, I will more or less imitate Twitter, and show a number and text to the 
side that says “followers.”

To do this well, I need to access to the database to access the followers of the logged user. To access the number of 
followers of a user, I will use a “group by”, or its equivalent in Query Set notation. Then, I will use a COUNT 
statement to count the number of users that appear on the “follows” column for all of the instances that the current 
user appears in “follower”. I need to check how to use COUNT and GROUP BY in Query Set notation.
	
To use COUNT in query set, I need to put “.count()” at the end of a filter() function (source: Mikhail Chernykh’s 
reply on 
https://stackoverflow.com/questions/15635790/how-to-count-the-number-of-rows-in-a-database-table-in-django#:~:text=You%20can%20either%20use%20Python's,the%20provided%20count()%20method.&text=You%20should%20also%20go%20through%20the%20QuerySet%20API%20Documentation%20for%20more%20information .)

I don’t need to save() the statement, since I’m not editing the database. I’m just getting data from the database.

This is similar to what I show on the “All Posts” page (the index.html file), but in this case, I will only show the 
posts that belong to the user whose name is in the profile page. That can be done with a “filter()”, and specifying 
that the user should be the one from the “username” parameter on the profile() view.

I’ll try comparing the logged user from the user in the profile page in the view(), NOT via Jinja notation. The keyword 
“request.user” stores the logged user. I don’t know if that’s an instance, or if it’s the username. So, I will create 
a Boolean variable that stores whether the “follow” button should be rendered. If the logged user has the same username 
than the user of the profile page, the Boolean variable will change to “false”. By default, it will be set to “true”. 
If the variable is “true”, and if the user’s signed in, I will render the “follow” button.

I think I know how to access the database to know whether to render the word “follow” or “unfollow” on the button. In 
the profile() view, I will check if the logged user is following the person in the profile page. If they aren’t, I 
will use a Boolean variable to render the word “follow”, and then send that variable to the page via Jinja. Otherwise, 
I will tell the Boolean variable that the word “unfollow” should be rendered. The actual word will be rendered via 
Jinja, depending on the state of the Boolean variable. 

The only thing that this will achieve will be to tell the page whether to render the word “follow” or “unfollow” when 
the user first enters the page. This will NOT change the button once the user clicks on the “follow/unfollow” button. 
The latter functionality will be done using JS.

I can’t use the same Boolean that I used for checking if the profile is the same user as the logged user, since that 
Boolean only tells me whether or not to render the button. So, I will have to create another Boolean variable.

It seems that, to have the possibility of getting an empty query from a Query Set statement, I need to use filter(), 
not get() (source: Niklas's question on 
https://stackoverflow.com/questions/1387727/checking-for-empty-queryset-in-django .)

To prevent any problems with React, and to avoid using two divs with the same ID, I will create a variable in my 
profile() view that says stores either the value “Follow” or “Unfollow”. Then, I will render that word directly into 
the button via Jinja notation by using notation like this:
    <button>{{variable_that_says_follow_unfollow}}</button>

Now, I need to paginate the posts whenever I enter into the profile of any person. That is, if I click the username of 
any user, I should only be able to see 10 of their posts. If I want to see more, I will need to click on “see more in 
page 2”. To do this, I will have to edit the profile() view.
	
I’ll need to check how I’m fetching the posts in the profile() view though, since I may get the same bug in profile() 
that I had in following_page(): that if a post doesn’t appear in the home page, that it won’t be rendered either in the 
profile page for that specific user, even if that user has posted less than 10 posts.

"""
def profile(request, username):

    # Check if the username exists
    try:
        existing_username = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "network/profile.html", {
            "error_message": "Error: That username does not exist."
        })

    # If the user exists, the error message won't be triggered
    error_message = ''

    # This tells me whether to render the follow button
    is_follow_active = True

    # This tells me whether to render "follow" or "unfollow"
    is_user_following_profile = False

    # This is a debugging message that checks if a user is following a person in a profile.
    is_user_following_query_set = ''

    # This will render the word "follow" or "unfollow" in the button itself
    follow_button_text = ''

    # This declares the variable that will store the logged user's username as a string
    logged_user_string = ''

    # this checks if the user's logged in, and whether if it's the same as the user in the profile page
    if request.user.is_authenticated:

        # This will send the user's username as a string in Jinja
        logged_user_string = str(request.user)

        if str(request.user) == str(existing_username):
            is_follow_active = False

        else:
            logged_user = request.user  # This stores the logged user

            # Instance of the person of the profile page
            profile_person = User.objects.get(username=existing_username)

            # This checks if the current user is following the person in the profile ...
            is_user_following_query_set = Follower.objects.filter(follower=logged_user, follows=profile_person)

            # If the user is not following the profile person, I will render the word "follow"
            if not is_user_following_query_set:
                is_user_following_profile = False
                follow_button_text = "Follow"
            else:
                is_user_following_profile = True
                follow_button_text = "Unfollow"


    # This obtains the number of people that the user is following
    number_of_people_that_user_follows = Follower.objects.filter(follower=existing_username).count()

    # This obtains the number of followers of the user in the profile
    number_of_followers = Follower.objects.filter(follows=existing_username).count()

    # This gets all the posts from the username that's displayed on the profile page
    all_posts_from_user = Post.objects.filter(user=existing_username).order_by('-timestamp')


    # This will paginate the posts so that each page has 10 posts
    paginated_posts = Paginator(all_posts_from_user, 10)

    # This gets the current paginated page
    # Prints "None" if I don't specify a page, or "1" if I add "1" as a parameter
    current_page_number = request.GET.get('page', 1)

    # This gets all the posts of the current page
    # Prints "<Page 1 of 2>"
    paginated_posts_in_current_page = paginated_posts.get_page(current_page_number)

    return render(request, "network/profile.html", {
        "username": existing_username,
        "error_message": error_message,
        "number_of_followers": number_of_followers,
        "number_of_people_that_user_follows": number_of_people_that_user_follows,
        "all_posts_from_user": all_posts_from_user,
        "is_follow_active": is_follow_active,
        "is_user_following_profile": is_user_following_profile,
        "is_user_following_query_set": is_user_following_query_set,
        "follow_button_text": follow_button_text,
        "paginated_posts_in_current_page": paginated_posts_in_current_page,
        "logged_user_string": logged_user_string,

    })

""" API for following or unfollowing a user

I will create the API routes for the Follow_or_unfollow() function. For that, I will create a new view(). That view 
will either insert an entry into the Follower table, or remove it. I could call the view something like “follow()”. 

I could put it in an URL called “/profile/username/follow/”. From that URL, I could get the username of the profile, so 
that the API knows the name of the user that I should follow or unfollow. To fix it a little bit, the URL should be 
something like “/profile/<str:username>/follow/”. 

I will need to make a call to the database before doing anything else. So, I will use a variable to call all of the 
followers, and one for all of the people that are being followed. This could be very similar to the code that I wrote 
for displaying the number of followers for a user.

I will first try following and unfollowing a user via a fetch() call by using vanilla JS. Afterwards, I will “translate” that 
code into React. The disadvantage of doing this is that, at first, the follower count won’t be updated. However, I can later 
re-do the “update follower count” by using another fetch() call to fix that, if I want to. 

Apparently, it doesn’t matter if I use a “submit” or a “onclick”: if I use a proper fetch() call, only a small part of the 
page will be updated.

I need 2 conditions on the API (on the follow() view) when detecting if the user clicked on the button: 1) detect if the user 
is following the person of the profile. If they are not, I will insert the logged user and the person of the profile in the 
Follower table in the database. 2) If the user’s already following the other person, I will stop following the other person. 
To do that, I will remove the logged user and the person of the profile from the Follower table. 

And remember to convert the data from the follow() view into JSON. I need to review the “mail” homework assignment. This is done 
when rendering the page in the follow() view. To convert the view code into JSON, I need to use code like the following (source 
of the code: my submission for the “mail” homework assignment):

    return JsonResponse([email.serialize() for email in emails], safe=False)

The rest of the code for the follow() view should have standard python code for a view.

I could try sending an empty POST request using a fetch() call. Then on the follow() view, I would check who the logged user is, 
and the username of the profile page. I can get the person of the profile from using “<str:” and a second parameter in the 
follow() view. Then, I would put an “if” statement checking if a POST request was sent. If it was, and the user is NOT following 
the person, I will put a Query Set statement. Otherwise, I will put another Query Set Statement. The queries will modify the 
Follower table.
	
Afterwards, I will send JSON data into the route (the URL that will only contain JSON code, which the user should not be able 
to access unless they manually type it on the URL bar.) That JSON code that was sent from the view will show the Follower table, 
and show if the current user and if the person of the profile are on the same entry. Then, by using an “if” statement on the 
fetch() call, I will check if the user is following the person on the profile. If they are, I will render the “unfollow” 
button. If they aren’t, I will render the “follow” button.
	
OR, to simplify matters, I will simply send one made-up JSON variable into the URL of the follow() view. I could call that 
variable “renderFollowButton”, and it could be a Boolean. If it’s true, I will render “Follow” in the button. Otherwise, I will 
render “Unfollow”. The JSON variable that I could send from the follow() view could be like this (source: “mail” homework):

    return JsonResponse({"variable_name": True/False }, status=200)
	
So, if I entered into “username/profile/follow”, I would only see a JS array saying “True” or “False”.

Then, by using the fetch() call, I would make the “if” statement to render “Follow/Unfollow”, depending on whether the variable 
says “True/False”. The “True/False” value would be stored in the “data” variable in the fetch() function. So, I will render 
“Follow” if data is equal to “True”, or “Unfollow” if it’s equal to “False”.

I think the most appropriate request for the “Follow/Unfollow” mechanic will be a POST request. Since whether a user can follow 
or unfollow another specific user is different for every user and should be private, then a POST request would be the most 
appropriate one.

To check whether a POST request was made from the profile.html file, I will use the following code snippet (source: my “mail” 
homework assignment):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

The user should be logged in other to follow or unfollow someone. So,, I’ll put a login decorator to the follow() view.

To delete a record from the database by using Query Set, I need to use the “.delete()” function (source: Wolph's reply from 
https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models .)

I will temporarily use "CSRF Exempt" to remove the CSRF protection to see if the CSRF protection is causing bugs 
in my JS code. I will later re-add the CSRF protection.

I will have to rebuild the button from scratch using React. I will also have to edit the follow() view so that, if the user enters the profile page, 
the “follow” or “unfollow” button will be rendered by using fetch(), NOT Jinja nor Django. To do that, I will modify the follow() view so that, if no 
POST request is sent, if the user’s following the person, JSON will send “true” and will render the “follow” button. Otherwise, it will send “false” 
in JSON and render “Unfollow”. That way, I won’t need to use Jinja to render the 1st time the “Follow” button.

"""
@csrf_exempt
@login_required
def follow(request, username):

    # Check if the username exists
    try:
        existing_username = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "network/profile.html", {
            "error_message": "Error: That username does not exist."
        })

    # This prints an error if the user accesses this URL without a POST request
    # if request.method != "POST":
    #     return JsonResponse({"error": "POST request required."}, status=400)


    logged_user = request.user  # This stores the logged user

    # Instance of the person of the profile page
    profile_person = User.objects.get(username=existing_username)

    # This checks whether the user is following the person in the profile in the Follower table
    is_user_following_query_set = Follower.objects.filter(follower=logged_user, follows=profile_person)

    # If the user enters the page and doesn't click on the "follow" button, this will automatically render the button
    if request.method != "POST":

        # If the user's not following the profile person, I will render the "follow" button
        if not is_user_following_query_set:
            return JsonResponse({"renderFollowButton": True}, status=200)

        # If the user's already following the person, I will render the "Unfollow" button
        else:
            return JsonResponse({"renderFollowButton": False}, status=200)


    # If the user's not following the profile person, I will insert them into the database to follow them
    if not is_user_following_query_set:

        # This prepares the data before inserting it into the database
        follow_user = Follower(follower=logged_user, follows=profile_person)

        # This inserts the data into the database
        follow_user.save()

        # Confirmation message
        follow_success_message = "You're now following this user!"

        # I will print the success message in the console
        print(follow_success_message)

        # This will change the button to "Unfollow" after inserting the user in the Follower table
        return JsonResponse({
            "renderFollowButton": False
            # "follow_success_message": follow_success_message
        }, status=200)

    # If the user's already following the profile person, they will be deleted from the Follower table
    else:
        # This deletes the entry in which the user is following the person in the profile
        is_user_following_query_set.delete()

        # Confirmation message
        follow_success_message = "You are no longer following this user."
        print(follow_success_message)


        # This will change the button to "Follow" after deleting the user from the Follower table
        return JsonResponse({"renderFollowButton": True}, status=200)

    # If the user enters the page without making a POST request, this might render as an alternative error message
    # return JsonResponse({
    #     "error": "The button won't say either 'Follow' nor 'Unfollow' for the time being."
    # }, status=400)

""" 'Following' page view.

I will add the "login required" decorator, since only logged users should be able to see this view.

To get all of the posts, I will use code similar to that of the index page. I will need to use a Query Set statement 
with the filter() function, instead of the all() one. The condition should be to look for all of the users that the 
logged user is following, and then fetch their posts. If it’s like in real social media apps, the posts should be in 
reverse chronological order.

To get the posts from the people that the logged user is following, I will need to 1st check the Follower table. I will 
need all instances where the logged user is present in the “follower” column. From those instances, I want all of the 
users present in the “follows” column.
	
Afterwards, I will get all fo the posts made by people whose user ID is in the group of people that are in the “follows” 
column for the logged user. I may need to use an array for this. Let me see if I can make a JOIN statement or a 
subquery using Query Set.
	
To do the query that I need to do, a subquery will suffice. Here’s how to make a subquery in Query Set (source: 
Ramast’s reply from https://stackoverflow.com/questions/8556297/how-to-subquery-in-queryset-in-django .) 

The sub query should work like this: “Give me all of the posts whose authors belong to the ‘follows’ column who are 
being followed by the logged user.” Translated into Query Set notation, the query would be like this:
    favorite_users_query = Follower.objects.filter(follower=logged_user_id).only('follows')
    posts_from_favorite_users = Post.objects.filter(user__in=favorite_users_query)

Turns out that I can’t access a foreign key with Query Set in the way I was trying to. Instead, I will need to use the 
“User” table to access the followers from the “Follower” table, and use notation like this  (source: alecxe's reply on 
https://stackoverflow.com/questions/27884129/django-queryset-foreign-key ):
    FK_Table.objects.filter(fk_variable__original_variable='variable_value')

Now, I just need to repeat the same pagination code for the posts in the follow_page() view as he one used in the 
index() view.

BUG: I have a bug with the following_page() view with the Paginator: to put it with an example, the user “sylveon” has 
at least 3 posts, and the 1st one says “Hello World”. However, that “Hello World” post never shows up in the “Following” 
page. That makes sense in the home page, since there are 11 posts in total, and “Hello World” was the 1st post in the 
web app. So, only 10 posts are properly showing up in the home page. However, if I only follow Sylveon, it doesn’t make 
sense that her “Hello World” post doesn’t show up, since Sylveon only has 3 posts in total. That happens because the 
pagination code is being executed the same as in the index() view. 

That happens because of the way that I’m printing the posts in the “Following” page: I’m using 2 “for” loops, but only 
via Jinja. Instead, I should create an array, and use the 2 “for” loops inside of the “following_page()” view to 
populate the array with the posts from the users that you’re following. Then, I should paginate the posts inside of 
that array. THEN, I should send that array with those posts via Jinja.  

I need to append to the array each post of the favorite users. The notation to append values to a Python list is:
    array.append(value_that_I_want_to_insert)
(source: my "commerce" homework assignment.)

"""
@login_required
def following_page(request):

    logged_user = request.user  # This gets the data from the logged user
    logged_user_id = logged_user.id  # ID of the user

    # This gets an instance of the logged user
    user_instance = User.objects.get(id=logged_user_id)

    # This will be populated with the 10 posts from the user's favorite accounts
    favorite_users_posts_array = []

    # This gets all the favorite users of the logged user
    favorite_users_query = Follower.objects.filter(follower__id=logged_user_id)

    # DEBUG message: this checks if the Query Set with the FK was created
    print(favorite_users_query)

    # DEBUG: this will let me see each item on the FK Query Set
    for favorite_user in favorite_users_query:
        print(favorite_user.id) # This prints "1537"
        print(favorite_user.follower)  # This prints "sylveon"

    # This gets all the posts from the favorite users of the logged user in reverse chronological order
    # posts_from_favorite_users = Post.objects.filter(user__in=favorite_user.follows).order_by('-timestamp')

    # This gets all the posts in reverse chronological order
    all_posts = Post.objects.all().order_by('-timestamp')

    # This will read all the posts from the user's favorite accounts, and then insert them in an array
    for post in all_posts:
        for favorite_user in favorite_users_query:
            if post.user == favorite_user.follows: 
                favorite_users_posts_array.append(post)



    # This will paginate the posts so that each page has 10 posts
    # paginated_posts = Paginator(all_posts, 10)

    # This will paginate the posts stored in the array
    paginated_posts = Paginator(favorite_users_posts_array, 10)

    # DEBUG msg: this prints the object that was created when I first called the Paginator class
    print(paginated_posts)

    # This gets the current paginated page
    # Prints "None" if I don't specify a page, or "1" if I add "1" as a parameter
    current_page_number = request.GET.get('page', 1)

    # DEBUG msg
    print(current_page_number)

    # This gets all the posts of the current page
    # Prints "<Page 1 of 2>"
    paginated_posts_in_current_page = paginated_posts.get_page(current_page_number)


    return render(request, "network/following.html", {
        "all_posts": all_posts,
        "favorite_users_query": favorite_users_query,
        "paginated_posts_in_current_page": paginated_posts_in_current_page,
    })

""" View for editing posts.

I need to create a new view, since the other view that creates posts inserts posts into the database, and I want to 
update the entries. I don’t want to add new entries when editing a post.
	
To make the post editing view, I will check for a POST request to add an extra layer of privacy when sending the 
request to edit the post. Remember that this question asks me to add security to the post edition mechanic. However, 
for the time being, I will use the decorator that removes CSRF protection to test that my API works. AFTERWARDS, I 
will re-add the CSRF protection, and make it work with the JS code.
	
If a POST request is made to the edition API, I will check the content of the body of the edited post. Then, I will 
update the entry that contains that specific post so that the “body” column is updated. That is, I will update the body 
of that post.

And, of course, only logged users can edit posts, so only logged users can use this function.

I will check of an additional parameter: the post’s ID number. So, alongside “request”, I will add another parameter to 
the edit() view.

What I need to do is to send via a POST request by using fetch(), and use stringify to send the body of the edited post. 
The first thing that I should so is use the stringify() function to get the text of the edited post, and insert it into a key, 
which should have the name of the column of the Post table that stores the body of a text. I also need the post’s ID number, 
so that I edit that specific post instead of any other post. 

So, I will need to use code like this (source: my submission for the “mail” homework assignment):

# index.html
  fetch('URL', {
      method: 'POST',
      headers: {
          'Accept': 'application/json, text/plain, */*',
          'Content-type':'application/json'
      },
      body:JSON.stringify({body:variable_that_stores_edited_post, post_id:post_id_number})                
  })

Afterwards, I need to get that JSON data into my edit_post() view, and convert it into a Python dictionary. That will be
done with the json.loads() function. I will use the following code snippet (source: my submission for the “mail” 
homework assignment):
# views.py
    data = json.loads(request.body)

Now, I have a Python dictionary called “data”, which contains a key called “body”, and a value which contains the text 
of the edited post. However, the only thing I want is the value, not the key nor the entire dictionary. To do that, I
will use Python’s get() function, and insert the “body” key as a parameter, and insert that into a variable (source: 
https://www.w3schools.com/python/ref_dictionary_get.asp .) So, I would use a code snippet like this:
    edited_post_variable = data.get("body")
	
I also need the post’s ID number. I will convert it into an int to avoid any issues when trying to insert it into the 
database. So, I will also use this code snippet:
    post_id = int(data.get("post_id"))

Finally, I will make a Query Set statement to update the Post table, so that I can edit that post in the database. I 
just realized that I need that post’s ID in order to edit that specific post. So, I will also include the post’s ID 
number in the JSON object, and I will insert that in a separate variable. I also want to make sure that the logged user 
is the only one who can edit their own posts, so I will filter the posts so that it looks for a post with its 
respective ID, which should be owned by the logged user. This can be done by using the filter 
“user=variable_with_request.user”. 

I also need to use the update() function at the end of the Query Set statement to update that post (source: my 
“commerce” homework assignment.) So, the Query Set Statement should be something like this: 
    Post.objects.filter(id=post_id, user=variable_with_request.user).update(body= edited_post_variable)

Note: I will include an “else” below the “if Method != POST” condition, since I will tell the code to only execute and 
make a Query Set query if the user makes a POST request (that is, if they click on the “Save” button.) Otherwise, the 
code should stop executing.

Remember: at first, I will deactivate the CSRF protection. But, if the above code works, I will reactivate it, and fix 
the bugs that show up along the way.

Note 2: I will need to add the JS code into the static folder (in “script.js”.) Otherwise, my JS code that contains the 
edit() and save() functions won’t execute in the logged user’s profile, so the users won’t be able to edit their own 
posts in the profile page otherwise. Also, that means I will have to reuse the IDs into the profile.html. It’s normally 
bad to re-use an ID for 2 or more different divs, but, since the posts from the home page are the exact same posts from 
the profile page (or, at least, the posts from the logged user), I could re-use the same ID for the same post that 
appears in both the home and the profile pages.
	
Also, if the same post in the different pages have different IDs, the edit() and save() function won’t execute. So, I 
would need to rewrite those 2 functions exclusively for the posts in the profile page, which would be extremely 
inefficient. So, I still prefer to use a same ID for the same post in the 2 different pages.

I need to return a JSON response in the edit_post() view, or otherwise, when I click on “Save”, the console will print 
me an error. I will use the following code snippet (source: my “mail” homework assignment):
    return JsonResponse({"message": "The post was edited successfully."}, status=201)


"""

@login_required
def edit_post(request, post_id):

    logged_user = request.user  # This gets the data from the logged user
    logged_user_id = logged_user.id  # ID of the user

    # This gets an instance of the logged user
    user_instance = User.objects.get(id=logged_user_id)

    # If the user enters the "/edit/number" page by typing "/edit/number" on the URL, this will render
    if request.method != "POST":
        return JsonResponse({"message": "You're not currently editing any posts"}, status=400)

    # If the user clicks on "Save", this will update the post
    else:

        # This converts the JSON data into a Python dictionary
        data = json.loads(request.body)

        print(data) # DEBUG msg

        edited_post_text = data.get("body") # This stores the post's body
        post_id = int(data.get("post_id"))  # This stores the post's ID

        print(edited_post_text) # DEBUG msg

        Post.objects.filter(id=post_id, user=user_instance).update(body=edited_post_text)

        # This returns JSON data to prevent a bug from happening
        return JsonResponse({"message": "The post was edited successfully."}, status=201)



""" Like and Unlike API.

I think I know what I need to do to finish the “like” functionality. To check whether to add or remove a like from a post, 
I will send a JSON response from the view to the JS code. That can be done with the JsonResponse function from Django/Python 
(source: https://docs.djangoproject.com/en/4.0/ref/request-response/ .) The variable that I will send via the JsonResponse 
function will be a Boolean. 

I think I get it: I will make a fetch call that will send to the view file two columns (2 variables): the id of the logged 
user, and the post ID. Then, in the API in the view, I will check if there’s an entry with that user ID and that post ID 
from the JSON data sent from the fetch() call. If it doesn’t exist, I will insert it into the databse, and I will add a 
like to the post. Otherwise, I will update the existing entry to that it subtracts one like from that post. 

"""
def like(request, post_id):
    pass

















""" 	Since the question says “on any page that displays posts”, that means that the 
Paginator functionality should work in both the index() and the follow_page() views. I 
could either create a separate function for creating the pagination, and then call it in 
both the index() and follow_page() views; or manually add the pagination in both views. 
The most efficient solution would be the former.

I’ll define the Paginator function separately, and I will call it in both the index() and follow_page() views before 
sending the Jinja variable to their respective .html files. To create the Paginator function, I first imported the 
Paginator library on top of the views file. Then I will create a function using “def”, but without adding a “request” 
parameter into it (source: https://www.w3schools.com/python/python_functions.asp .) However, I still have to ad a 
parameter to it, since I will call the variable that contains all of the posts that will be displayed via Jinja on the 
.html pages.
	
So, I will add a parameter to the new function that I’ll create. That parameter will store all of the posts of that 
page. Next, I will call the Paginator class, and I will insert into it the variable with all of the posts, and the 
number “10”, since I only want 10 posts per page, and I will insert that into a variable (source: 
https://docs.djangoproject.com/en/4.0/topics/pagination/ .) So, I would use a snippet like the following:
    paginated_variable = Paginator(posts, 10)
	
Inserting all of the pages in the html files will be tricky. I will need to use 2 “for” loops. The 1st for loop will 
check how many pages are in total (this will depend on the number of posts.) Then, the 2nd  for loop will store all of 
the posts in each page. To get the number of pages created, I need to use the following snippet: 
    paginated_variable.page_range 

Then, to get each individual post, I would need to use the following snippet:
    paginated_variable.page(number).object_list

So, to get all of the posts from all of the pages, I would need to create 2 for loops, and nest one inside of the other.

I may add “print()” statements to debug my code to see if the correct number of posts are being stored inside of each 
page.

Once I finish executing the pagination() function, I will call the return() python function so that the index() and 
follow_page() views get the paginated posts. Source of the snippet that I will use for calling the return function: 
https://www.w3schools.com/python/ref_keyword_return.asp 

What I tried to do didn’t work. I will try doing something else that I saw on the Paginator documentation. I will first 
go to one of the two views in which I will need to paginate the views. Then, I will call the Paginator() call on the 
variable that stores all of the posts. Then, I will store the page number in a variable that has the following code: 
    request.GET.get('page')

Next, I will create yes another variable, I which I will call the page number. To do that, I will insert the following 
snippet inside of the new variable:
    paginated_variable.get_page(page_number)

Finally, in the return() function of the view(), I will send the variable via Jinja notation.

Source of the code from the previous 3 paragraphs: https://docs.djangoproject.com/en/4.0/topics/pagination/ 

"""
# def paginate(posts):
#     paginated_posts = Paginator(posts, 10)
#
#     # DEBUG msg: this prints the object that was created when I first called the Paginator class
#     print(paginated_posts)
#
#     # This gets the current paginated page
#     current_page_number = request.GET.get('page')
#
#     # This gets all the posts of the current page
#     page_posts = paginated_posts.get_page(current_page_number)
#
#     return page_posts