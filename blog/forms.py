from django import forms
from .models import Hashtag, Post,Comment 

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'writer', 'body','hashtags','image']

class CommentForm(forms.ModelForm) :
    class Meta:
        model = Comment
        fields = ['text']

class HashtagForm(forms.ModelForm):
    class Meta:
        model = Hashtag
        fields = ['name']