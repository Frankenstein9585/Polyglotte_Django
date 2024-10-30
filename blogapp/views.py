from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import BlogPost, User
from .forms import PostForm


# Create your views here.
def index(request):
    posts = BlogPost.objects.order_by('-created_at')
    return render(request, 'index.html', {'posts': posts})


def show_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'post_page.html', {'post': post})


@login_required
def new_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            if post.category == '':
                post.category = 'Miscellaneous'
            post.save()
            messages.success(request, 'Post Successfully Created')
            return redirect('index')
    return render(request, 'create_post.html', {
        'title': 'New Post',
        'form': form,
        'legend': 'New Post'
    })


@login_required
def update_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.user != request.user:
        raise PermissionDenied
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully updated your blogpost')
            return redirect('show_post', post_id=post.id)

    return render(request, 'create_post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.user != request.user:
        raise PermissionDenied
    post.delete()
    messages.success(request, 'Your post has been deleted.')
    return redirect('index')
