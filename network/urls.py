
from django.urls import path

from . import views

""" I need to add the URL of the profile page.

To insert the username as a parameter, that needs to be done from the urls.py file. The URL should display the username 
of the profile page of the user that a person clicks on the web app. I think I will need to use the “<str:” notation 
in urls.py.

I could put it in an URL called “/profile/username/follow/” to call the follow() API. From that URL, I could get the 
username of the profile, so that the API knows the name of the user that I should follow or unfollow. To fix it a 
little bit, the URL should be something like “/profile/<str:username>/follow/”. 

I don’t need to insert the name of the logged user into the URL for the "following_page()" URL, since I can already get 
the logged user via Django in its respective view. So, I don’t need to inert an extra parameter in the URL. 
	
I need to create a new URL for the edit() view. This URL will only contain JSON data, but I still need to create the 
URL. It will be the same as the follow() view. I will use that views as a reference to see how to convert and fetch 
JSON data. Since I need the post’s ID number as a parameter, I will also include the post ID number on the URL that 
calls the edit_post() view.

I will have to create a new URL to access the “like” API from the views.py file. I will add the URL in the urls.py 
file. The URL will be similar to the “edit” one, but it will instead be called “like”.

"""
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:username>/follow", views.follow, name="follow"),
    path("following", views.following_page, name="following_page"),
    path("edit/<str:post_id>", views.edit_post, name="edit_post"),
    path("like/<str:post_id>", views.like, name="like"),

]

