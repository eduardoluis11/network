
from django.urls import path

from . import views

""" I need to add the URL of the profile page.

To insert the username as a parameter, that needs to be done from the urls.py file. The URL should display the username 
of the profile page of the user that a person clicks on the web app. I think I will need to use the “<str:” notation 
in urls.py.

"""
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
]
