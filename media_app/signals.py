
from .models import VideoModel
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .tasks import convert_to_480p, convert_to_720p
import os
from pathlib import Path
import django_rq


@receiver(post_save, sender=VideoModel)
def video_post_Save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('video_conferter', autocommit=True)
        queue.enqueue( convert_to_480p, instance.video_file.path)
        queue.enqueue( convert_to_720p, instance.video_file.path)


@receiver(post_delete, sender=VideoModel)
def video_auto_delete(sender, instance, **kwargs):
    if instance.video_file:

        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            os.remove(instance.thumbnail_url.path)

        source_path = Path(instance.video_file.path)
        path_480p = source_path.with_stem(f"{source_path.stem}_480p")
        path_720p = source_path.with_stem(f"{source_path.stem}_720p")

        if os.path.isfile(path_480p):
            os.remove(path_480p)
        if os.path.isfile(path_720p):
            os.remove(path_720p)
