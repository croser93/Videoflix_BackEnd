from django.db import models


class VideoModel(models.Model):

    title   = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    video_file = models.FileField(upload_to="videos/")
    thumbnail_url = models.ImageField(upload_to="thumbnails/")
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title