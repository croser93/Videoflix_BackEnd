from django.contrib import admin
from .models import VideoModel


@admin.register(VideoModel)
class VideoModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'created_at']
