
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
	
"""
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following_page, name="following_page"),
]

