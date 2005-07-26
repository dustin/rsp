from django.conf.urls.defaults import *

# Base for all released things
info_dict = {
    'app_label': 'blog',
    'module_name': 'posts',
    'date_field': 'post_date',
    'extra_lookup_kwargs': {'released__exact': True},
}

urlpatterns = patterns('',

    (r'^archive/(?P<year>\d{4})/(?P<month>\d)/$',
        'django.views.generic.date_based.archive_month',
            dict(info_dict, use_numeric_months=True)),
    (r'^archive/(?P<year>\d{4})/$',
        'django.views.generic.date_based.archive_year', info_dict),

    # Get an individual post
    (r'^post/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/(?P<object_id>\d+)/$',
        'django.views.generic.date_based.object_detail',
            dict(info_dict, template_name='post',
            use_numeric_months=True, extra_lookup_kwargs={})),

    (r'^rss/', 'blog.apps.blog.views.fetch.showRecentReleased',
        {'tmpl': 'rss', 'ctype': 'text/xml'}),
    (r'^all/', 'django.views.generic.date_based.archive_index',
        dict(info_dict, extra_lookup_kwargs={})),
    (r'^$', 'django.views.generic.date_based.archive_index',
        dict(info_dict, template_name='index', num_latest=10)),
)
