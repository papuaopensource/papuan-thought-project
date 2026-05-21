from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Comment, Reaction, Follow, Bookmark, Notification


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ("author", "essay", "parent", "created_at")
    search_fields = ("author__username", "content", "essay__title")
    raw_id_fields = ("essay", "author", "parent")


@admin.register(Reaction)
class ReactionAdmin(ModelAdmin):
    list_display = ("user", "essay", "reaction_type", "created_at")
    list_filter = ("reaction_type",)
    raw_id_fields = ("essay", "user")


@admin.register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ("follower", "following", "created_at")
    raw_id_fields = ("follower", "following")


@admin.register(Bookmark)
class BookmarkAdmin(ModelAdmin):
    list_display = ("user", "essay", "created_at")
    raw_id_fields = ("user", "essay")


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ("recipient", "sender", "notification_type", "is_read", "created_at")
    list_filter = ("notification_type", "is_read")
    raw_id_fields = ("recipient", "sender", "essay")
