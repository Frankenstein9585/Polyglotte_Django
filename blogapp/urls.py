from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('post/<int:post_id>/', views.show_post, name='show_post'),
    path('post/', views.new_post, name='new_post'),
    path('post/edit/<int:post_id>/', views.update_post, name='update_post'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
]
