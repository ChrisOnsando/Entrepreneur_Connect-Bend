from django.urls import path

from app.posts.views import (
    PostListView, 
    PostListAllView,
    PostDetailView,
    PostCommentView,
    PostCommentDetailView,
    PostLikeView,
    PostDislikeView,
)

urlpatterns = [
    path("post/", PostListView.as_view(), name="post-list"),
    path("posts/", PostListAllView.as_view(), name="all-posts"),
    path(
        "post/<str:post_id>/",
        PostDetailView.as_view(),
        name="post-detail",
    ),
    path("comments/", PostCommentView.as_view(), name="comment"),
    path(
        "comments/<str:post_id>/",
        PostCommentDetailView.as_view(),
        name="comment-delete",
    ),
     path(
        "likes/<str:post_id>/like/",
        PostLikeView.as_view(),
        name="like",
    ),
    path(
        "dislikes/<str:post_id>/dislike/",
        PostDislikeView.as_view(),
        name="dislike",
    ),
]
