import os
from channels.asgi import get_channel_layer
from django.conf import settings

PROJECT_NAME = os.environ.get('PROJECT_NAME')
PROJECT_SETTINGS = '{0}.settings'.format(PROJECT_NAME)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", PROJECT_SETTINGS)
channel_layer = get_channel_layer()