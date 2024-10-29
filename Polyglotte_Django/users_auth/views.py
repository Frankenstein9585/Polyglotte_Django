from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm


# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.info(request, 'You have successfully logged in!')
            return redirect('index')
        else:
            messages.error(request, 'There was an error logging in, Try Again!')
            return redirect('login')
    return render(request, 'signin.html', {})


def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('index')


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Registration Successful. You can now login')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})
