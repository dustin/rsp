from django.conf.urls.defaults import *
from blog.apps.blog.models import Post
from blog import blogfeeds

# Base for all released things
info_dict = {
    'queryset': Post.objects.filter(released__exact=True),
    'date_field': 'post_date',
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
    (r'^post/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d+)/(?P<slug>[-\w]+)/$',
        'django.views.generic.date_based.object_detail',
            dict(info_dict, template_name='post.html', slug_field='slug',)),

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
        {'template_name': 'index.html',
            'queryset': Post.objects.all(), 'date_field': 'post_date'}),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^$', 'django.views.generic.date_based.archive_index',
        dict(info_dict, template_name='index.html', num_latest=10)),
)
