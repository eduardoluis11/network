from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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

    # This obtains the number of followers of the logged user
    number_of_followers = Follower.objects.filter(follower=existing_username).count()

    return render(request, "network/profile.html", {
        "username": existing_username,
        "error_message": error_message,
        "number_of_followers": number_of_followers,

    })