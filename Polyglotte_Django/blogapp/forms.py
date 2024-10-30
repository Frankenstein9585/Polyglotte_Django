from django import forms
from .models import BlogPost
from ckeditor.fields import RichTextField


class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'subheading', 'category', 'content']
