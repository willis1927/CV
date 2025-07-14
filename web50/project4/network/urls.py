
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("user/<int:user_id>", views.get_user, name="get_user"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("following/<int:user_id>", views.following, name="following"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("likes", views.update_likes, name="update_likes")
]
