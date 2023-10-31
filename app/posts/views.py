from typing import Any

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from app.posts.models import(
    Post,
    PostComment,
) 
from app.posts.permissions import IsOwnerOrReadOnly
from app.posts.serializers import (
    PostSerializer,
    PostCommentSerializer,
    LikeSerializer,
    DislikeSerializer,
)
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import UpdateAPIView

class PostListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
   
class PostListAllView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "post_id"

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Returns message on deletion of posts
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Post deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

class PostLikeView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer
    queryset = Post.objects.all()
    lookup_field = "post_id"
    renderer_classes = (JSONRenderer,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Post liked successfully",
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDislikeView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DislikeSerializer
    queryset = Post.objects.all()
    lookup_field = "post_id"
    renderer_classes = (JSONRenderer,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Post disliked successfully",
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostCommentView(generics.ListCreateAPIView):
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()
    permission_classes = [IsAuthenticated]
    renderer_classes = (JSONRenderer,)


class PostCommentListView(generics.ListAPIView):
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()
    permission_classes = [IsAuthenticated]
    renderer_classes = (JSONRenderer,)


class PostCommentListDetailView(generics.ListAPIView):
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()
    permission_classes = [IsAuthenticated]
    renderer_classes = (JSONRenderer,)
    lookup_field = "post_id"


class PostCommentDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()
    renderer_classes = (JSONRenderer,)
    permission_classes = [IsAuthenticated]
    lookup_field = "post_id"

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Returns message on deletion of comments
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Comment deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    
