# Django settings for blog project.

DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

LANGUAGE_CODE = 'en-us'

DATABASE_ENGINE = 'postgresql' # 'postgresql', 'mysql', or 'sqlite3'.
DATABASE_NAME = 'blog'             # Or path to database file if using sqlite3.
DATABASE_USER = 'blog'             # Not used with sqlite3.
DATABASE_PASSWORD = 'blogpw'         # Not used with sqlite3.
DATABASE_HOST = 'db'             # Set to empty string for localhost. Not used with sqlite3.

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hwrb#n(%$!x8a($+x&@50mavo!(&nr$%$74%$_q1_!o==-c)9s'

ROOT_URLCONF = 'blog.settings.urls.main'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    "/data/web/django/templates/blog/",
)

INSTALLED_APPS = (
    'blog.apps.blog',
)
