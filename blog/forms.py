from django import forms
from .models import Comment, Post

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','tags',  'body']


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','tags',  'body']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class SearchForm(forms.Form):
    query = forms.CharField()