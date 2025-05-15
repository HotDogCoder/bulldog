import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from django.core.wsgi import get_wsgi_application
from wfastcgi import WSGIContainer, run

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

if __name__ == '__main__':
    run()