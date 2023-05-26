import os

from django.core.wsgi import get_wsgi_application

from stats.utils import InitData

init = InitData()
init.run()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samdu_stats.settings')

application = get_wsgi_application()
