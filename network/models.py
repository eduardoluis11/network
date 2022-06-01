from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

""" I will work with 4 tables: one for the users, one for the posts, one for the likes, and one for the followers. Out 
of those 4, the User table is already created.

Relationships:
•	Posts and Users: One-to-Many.
•	Users and Users (Followers): Many-to-Many.
•	Posts and Likes: One-to-Many.
•	Likes and Users: One-to-Many.

Columns: 
	I will need the following columns for each table.
	
•	Posts: ID of the user who made the post, number of likes, timestamp of the time when the post was created, and the 
text of that post.

•	Followers: user ID, and the ID of the person that the current user is following. Multiple entries can have the same 
user ID, since a single user can follow multiple people.

•	Likes: ID of the user who gave a like, and ID of the post that received the like.

I will leave the names in singular, since the admin panel will add them an "S" at the end of the name to make them
plural.
"""

""" Post model.

For the "user", "body", and "timestamp" columns, I will use some code snippets from my homework submission for the 
Mail project (source: https://github.com/me50/eduardoluis11/tree/web50/projects/2020/x/mail .)

The number of likes will be an integer. I won’t have any decimals. So, I will have to use the “IntegerField” field to 
store the number as an integer (source: https://www.geeksforgeeks.org/integerfield-django-models/ .)
"""
class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    number_of_likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

""" Follower model.
"""
class Follower(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_who_follows")
    follows = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_being_followed")
