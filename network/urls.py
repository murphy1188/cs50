
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("<str:username>/following", views.following_posts_page, name="following_posts"),

    # API Routes
    path("posts", views.new_post, name="new_post"),
    path("posts/<str:username>", views.posts, name="user_posts"),
    path("postss/<int:id>", views.like, name="likes"),
    path("posts/comments/<int:id>", views.comment, name="comments"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("user/<str:username>/following/posts", views.following_posts, name="following")
]
