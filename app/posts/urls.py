from django.urls import path

from app.posts.views import (
    PostListView, 
    PostListAllView,
)

urlpatterns = [
    path("post/", PostListView.as_view(), name="post-list"),
    path("posts/", PostListAllView.as_view(), name="all-posts"),
]