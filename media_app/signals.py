
from .models import VideoModel
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=VideoModel)
def video_post_Save(sender, instance, created, **kwargs):
    print('video wurde gespeichert')
    if created:
        print('video created')