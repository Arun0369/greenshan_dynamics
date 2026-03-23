"""
WSGI config for greenshan_project project.
"""

import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greenshan_project.settings')

# Setup Django
django.setup()

# 🔥 AUTO MIGRATE (THIS FIXES YOUR ERROR)
from django.core.management import call_command
call_command('migrate', interactive=False)

# WSGI application
application = get_wsgi_application()