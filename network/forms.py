# This contains the Django forms of the web app

from django import forms
from .models import Post, Like, Follower

""" Form for creating posts.

I will give it a character limit of 300 characters to imitate Twitter's character limit.

Source of the code snippet for creating new posts: my homework assignment submission
for the "commerce" project for Web50: https://github.com/me50/eduardoluis11/tree/web50/projects/2020/x/commerce
"""
class CreatePostForm(forms.Form):
    new_post = forms.CharField(max_length=300, widget=forms.Textarea)