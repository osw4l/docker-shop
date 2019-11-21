from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'backend.apps.app'

    def ready(self):
        from . import signals

