from django.conf.urls.defaults import *
from rockstar import blogfeeds

# Base for all released things
info_dict = {
    'app_label': 'blog',
    'module_name': 'posts',
    'date_field': 'post_date',
    'extra_lookup_kwargs': {'released__exact': True},
}

feeds = {
    'full': blogfeeds.Full,
    'summary': blogfeeds.Summary,
    'fullunreleased': blogfeeds.Unreleased,
    'comments': blogfeeds.Comments,
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
    # The following two are for backwards compatibility.
    (r'^rss/$', 'django.contrib.syndication.views.feed',
        {'url': 'summary', 'feed_dict': feeds}),
    (r'^rssfull/', 'django.contrib.syndication.views.feed',
        {'url': 'full', 'feed_dict': feeds}),
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),

    (r'^comments/', include('django.contrib.comments.urls.comments')),

    (r'^all/', 'django.views.generic.date_based.archive_index',
        dict(info_dict, template_name='index', extra_lookup_kwargs={})),
    (r'^admin/', include('django.contrib.admin.urls.admin')),
    (r'^$', 'django.views.generic.date_based.archive_index',
        dict(info_dict, template_name='index', num_latest=10)),
)
