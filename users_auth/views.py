from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UpdateForm, BioForm
from blogapp.models import BlogPost


# Create your views here.
def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
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
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Registration Successful. You can now login')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})


@login_required
def user_account(request):
    user = request.user
    update_form = UpdateForm(instance=user)
    bio_form = BioForm()

    if request.method == 'POST':
        if 'update' in request.POST:
            update_form = UpdateForm(request.POST, instance=user)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, 'Your account has successfully been updated')
                return redirect('account')
        elif 'bio' in request.POST:
            bio_form = BioForm(request.POST, instance=user)
            if bio_form.is_valid():
                # print(bio_form.data)
                # user.bio = bio_form.cleaned_data['bio']
                # user.save()
                bio_form.save()
                messages.success(request, 'Your bio has successfully been updated')
                return redirect('account')

    # bio_form.fields['bio'].initial = user.bio

    posts = BlogPost.objects.filter(user=user).order_by('-created_at')

    return render(request, 'profile_page.html', {
        'update_form': update_form,
        'bio_form': bio_form,
        'posts': posts
    })
