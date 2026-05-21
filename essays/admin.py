from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Essay, Tag


@admin.register(Essay)
class EssayAdmin(ModelAdmin):
    list_display = ("title", "author", "status", "is_featured", "published_at", "created_at")
    list_filter = ("status", "is_featured")
    search_fields = ("title", "author__username", "content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    date_hierarchy = "created_at"
    raw_id_fields = ("author",)


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
