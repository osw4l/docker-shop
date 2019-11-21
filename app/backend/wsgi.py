import os
from dj_static import Cling
from django.core.wsgi import get_wsgi_application

PROJECT_NAME = os.environ.get('PROJECT_NAME')
PROJECT_SETTINGS = '{0}.settings'.format(PROJECT_NAME)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", PROJECT_SETTINGS)

application = Cling(get_wsgi_application())
