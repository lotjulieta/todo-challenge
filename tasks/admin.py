from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_completed", "created_at")
    search_fields = ("title", "description", "user__username")
    list_filter = ("is_completed", "created_at", "user")
    readonly_fields = ("created_at",)
