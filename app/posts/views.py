from typing import Any

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from app.posts.models import Post
from app.posts.permissions import IsOwnerOrReadOnly
from app.posts.serializers import (
    PostSerializer,
)


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

