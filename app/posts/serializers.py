
from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.posts.models import(
    Post, 
    Tag, 
    PostComment,
)
from app.user.serializers import UserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50,
    )

    class Meta:
        model = Tag
        fields = ("name")


class PostSerializer(serializers.ModelSerializer):
    post_id = serializers.CharField(
        read_only=True,
    )
    author = UserSerializer(read_only=True)
    image = serializers.CharField(
        min_length=5,
    )
    body = serializers.CharField(
        min_length=5,
    )
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )  # type: ignore[var-annotated]
    taglist = serializers.CharField(
        write_only=True,
    )
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = (
            "post_id",
            "author",
            "image",
            "body",
            "tags",
            "taglist",
            "likes_count",
            "dislikes_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
            "tags",
            "author",
        )
    def create(self, validated_data: Any) -> Any:
        """set current user as author"""
        validated_data["author"] = self.context.get("request").user  # type: ignore[union-attr]
        taglist = validated_data.pop("taglist")
        post = super().create(validated_data)
        tags = []
        for name in taglist.split(","):
            tag, _ = Tag.objects.get_or_create(name=name.strip())
            tags.append(tag)
        post.tags.set(tags)

        return post

    def get_likes_count(self, instance: Any) -> Any:
        return instance.likes.count()
    def get_dislikes_count(self, instance: Any) -> Any:
        return instance.dislikes.count()
    
class LikeSerializer(serializers.Serializer):
    def update(self, instance: Any, validated_data: Any) -> Any:
        """
        update the likes of an post
        """
        request = self.context.get("request")

        if request.user in instance.likes.all():  # type: ignore[union-attr]
            instance.likes.remove(request.user)  # type: ignore[union-attr]
            return instance
        if request.user in instance.dislikes.all():  # type: ignore[union-attr]
            instance.dislikes.remove(request.user)  # type: ignore[union-attr]
        instance.likes.add(request.user)  # type: ignore[union-attr]
        return instance

class DislikeSerializer(serializers.Serializer):
    def update(self, instance: Any, validated_data: Any) -> Any:
        """update the dislikes of a post"""
        request = self.context.get("request")

        if request.user in instance.dislikes.all():  # type: ignore[union-attr]
            instance.dislikes.remove(request.user)  # type: ignore[union-attr]
            return instance
        if request.user in instance.likes.all():  # type: ignore[union-attr]
            instance.likes.remove(request.user)  # type: ignore[union-attr]
        instance.dislikes.add(request.user)  # type: ignore[union-attr]
        return instance
    
class PostCommentSerializer(serializers.ModelSerializer):
    """
    Comments Serializer
    """

    commenter = UserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = (
            "id",
            "commenter",
            "comment",
            "post",
            "created_at",
        )
        read_only_fields = (
            "created_at",
            "commenter",
            "id",
        )

    def create(self, validated_data: Any) -> Any:
        request = self.context["request"]
        validated_data["commenter"] = request.user
        instance = PostComment.objects.create(**validated_data)
        return instance
