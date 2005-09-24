from django.conf.urls.defaults import *

# Base for all released things
info_dict = {
    'app_label': 'blog',
    'module_name': 'posts',
    'date_field': 'post_date',
    'extra_lookup_kwargs': {'released__exact': True},
}

urlpatterns = patterns('',

    (r'^archive/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        'django.views.generic.date_based.archive_month',
            dict(info_dict)),
    (r'^archive/(?P<year>\d{4})/$',
        'django.views.generic.date_based.archive_year', info_dict),

    # Get an individual post
    (r'^post/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d+)/(?P<slug>\w+)/$',
        'django.views.generic.date_based.object_detail',
            dict(info_dict, template_name='post', slug_field='slug',
            extra_lookup_kwargs={})),

    # Django RSS
    (r'^rss/', include('django.conf.urls.rss')),

    (r'^all/', 'django.views.generic.date_based.archive_index',
        dict(info_dict, template_name='index', extra_lookup_kwargs={})),
    (r'^$', 'django.views.generic.date_based.archive_index',
        dict(info_dict, template_name='index', num_latest=10)),
)
