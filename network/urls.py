
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('users/<str:username>', views.userProfile, name='userProfile'),
    path('makefriendship', views.make_friendship, name='make_friendship'),
    path('liking/<str:post_title>', views.liking, name='liking'),
    path('unliking/<str:post_title>', views.unliking, name='unliking'),
    path('posts/users/<str:username>', views.userPost, name='userPost'),
    path('userFriendship/<str:username>', views.userFriendship, name='userFriendship'),
    path('myFollowing', views.myFollowing, name='myFollowing'),
    path('posts', views.compose, name='compose'),
    path('updatePost/posts/<int:pk>', views.updatePost, name='updatePost'),
    path('posts/all', views.all_post, name='all_post'),
]

