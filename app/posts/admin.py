from django.contrib import admin

from app.posts.models import Post, Tag

admin.site.register(Tag)
admin.site.register(Post)
