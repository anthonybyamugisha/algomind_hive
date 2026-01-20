"""
WSGI config for algomind_hive project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Check if deployment settings should be used
if os.environ.get('DEPLOYMENT_ENV') == 'azure':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'algomind_hive.deployment_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'algomind_hive.settings')

application = get_wsgi_application()
