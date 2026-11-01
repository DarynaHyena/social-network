from django import forms
from posts.models import Posts, Comment, Like

class PostForm(forms.ModelForm):
  class Meta:
    model = Posts
    fields = ['title', 'content','community']

    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control'}),
      'content': forms.Textarea(attrs={'class': 'form-control'}),
      'community': forms.Select(attrs={'class': 'form-control'}),
    }


class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['content']

    widgets = {
      'content': forms.Textarea(attrs={'class': 'form-control'}),
    }
