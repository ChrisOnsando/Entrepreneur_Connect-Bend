
from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.posts.models import Post, Tag
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
