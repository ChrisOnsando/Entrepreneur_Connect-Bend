import uuid
from typing import Any

from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save

from app.abstracts import TimeStampedModel

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name

class Post(TimeStampedModel):
    post_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        max_length=255,
        primary_key=True,
    )
    image = models.TextField(blank=True, null=True)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name="tags")
    likesCount = models.BigIntegerField(
        blank=True,
        default=0,
    )
    likes = models.ManyToManyField(
        User, related_name="likes", blank=True
    )
    dislikes = models.ManyToManyField(
        User, related_name="dislike", blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
