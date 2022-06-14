from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# This will let me send and receive JSON data (source: my "mail" homework assignment)
from django.http import JsonResponse

# This adds the "CSRF exempt" function (source: my "mail" homework assignment)
from django.views.decorators.csrf import csrf_exempt

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
 
"""
def index(request):

    # This gets all the posts from the database
    all_posts = Post.objects.all().order_by('-timestamp')

    # This calls the post creation form
    form = CreatePostForm()

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
        })


    return render(request, "network/index.html", {
        "form": form,
        "all_posts": all_posts,
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

    # this checks if the user's logged in, and whether if it's the same as the user in the profile page
    if request.user.is_authenticated:
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
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)


    logged_user = request.user  # This stores the logged user

    # Instance of the person of the profile page
    profile_person = User.objects.get(username=existing_username)

    # This checks whether the user is following the person in the profile in the Follower table
    is_user_following_query_set = Follower.objects.filter(follower=logged_user, follows=profile_person)

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
    return JsonResponse({
        "error": "The button won't say either 'Follow' nor 'Unfollow' for the time being." 
    }, status=400)