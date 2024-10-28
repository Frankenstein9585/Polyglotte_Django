from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import BlogPost, User


# Create your views here.
def index(request):
    posts = BlogPost.objects.order_by('-created_at')
    return render(request, 'index.html', {'posts': posts})


def show_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)  # This will correctly fetch the post using UUID
    return render(request, 'show_post.html', {'post': post})

