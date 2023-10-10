import uuid
from typing import Any

from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

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
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    image = CloudinaryField("post_images", blank=True, null=True)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name="tags")
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="author", null=True
    )
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


@receiver(pre_save, sender=Post)
def slug_pre_save(sender: Any, instance: Any, **kwargs: Any) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.post_id}")