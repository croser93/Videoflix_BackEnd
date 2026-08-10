
from .models import VideoModel
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .tasks import convert_to_480p, convert_to_720p, convert_to_1080p
from pathlib import Path
import os
import django_rq
import shutil


@receiver(post_save, sender=VideoModel)
def video_post_Save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_to_480p, instance.video_file.path, instance.id)
        queue.enqueue(convert_to_720p, instance.video_file.path, instance.id)
        queue.enqueue(convert_to_1080p, instance.video_file.path, instance.id)


@receiver(post_delete, sender=VideoModel)
def video_auto_delete(sender, instance, **kwargs):
    if instance.video_file:

        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            os.remove(instance.thumbnail_url.path)

        source_path = Path(instance.video_file.path)
        path_name = source_path.parent / str(instance.id) 

        if path_name.exists():
            shutil.rmtree(path_name)

