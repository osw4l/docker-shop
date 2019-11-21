#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    PROJECT_NAME = os.environ.get('PROJECT_NAME')
    PROJECT_SETTINGS = '{0}.settings'.format(PROJECT_NAME)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", PROJECT_SETTINGS)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)