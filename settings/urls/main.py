from django.conf.urls.defaults import *

info_dict = {
    'app_label': 'blog',
    'module_name': 'posts',
    'date_field': 'post_date',
}

urlpatterns = patterns('',
    # Example:
    # (r'^blog/', include('blog.apps.foo.urls.foo')),

    (r'^archive/(?P<year>\d{4})/(?P<month>[A-z]{3})/$',
        'django.views.generic.date_based.archive_month', info_dict),
    (r'^archive/(?P<year>\d{4})/$',
        'django.views.generic.date_based.archive_year',  info_dict),
    (r'^archive/$', 'django.views.generic.date_based.archive_index', info_dict),

    (r'^rss/', 'blog.apps.blog.views.fetch.showRecentReleased',
        {'tmpl': 'rss', 'ctype': 'text/xml'}),
    (r'^post/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/(?P<post_id>\d+)/$',
        'blog.apps.blog.views.fetch.getArticle'),
    (r'^all/', 'blog.apps.blog.views.fetch.showRecentAll'),
    (r'^$', 'blog.apps.blog.views.fetch.showRecentReleased'),
)
