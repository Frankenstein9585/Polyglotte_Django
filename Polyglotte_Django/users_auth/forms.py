from django import forms
from django.contrib.auth.forms import UserCreationForm
from blogapp.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
