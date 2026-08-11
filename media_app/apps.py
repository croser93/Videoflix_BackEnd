from django.apps import AppConfig


class MediaAppConfig(AppConfig):
    name = 'media_app'

    def ready(self):
        from . import signals
