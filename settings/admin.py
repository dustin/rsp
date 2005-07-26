# Django settings for blog project admin site.

from main import *

TEMPLATE_DIRS = (
    '/usr/local/lib/python2.4/site-packages/django-1.0.0-py2.4.egg/django/conf/admin_templates',
    # Put strings here, like "/home/html/django_templates".
)
ROOT_URLCONF = 'blog.settings.urls.admin'
MIDDLEWARE_CLASSES = (
    'django.middleware.admin.AdminUserRequired',
    'django.middleware.common.CommonMiddleware',
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'
