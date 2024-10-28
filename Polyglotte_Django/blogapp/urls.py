from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('post/<uuid:post_id>/', views.show_post, name='show_post')
]
