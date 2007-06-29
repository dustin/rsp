from django.conf.urls.defaults import *
from django.contrib.sitemaps import Sitemap, GenericSitemap
from rockstar.apps.blog.models import Post
from rockstar import blogfeeds

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

class SpecificPage(Sitemap):
    def __init__(self, path, priority=0.7, freq='daily'):
        self.location=path
        self.changefreq=freq
        self.lastmod=Post.objects.latest('post_date').post_date
        self.priority=priority

    def items(self):
        return [self]

sitemaps = {
    'index': SpecificPage('/'),
    'blog': GenericSitemap(info_dict, priority=0.6),
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

    (r'^xml_rpc_srv/$', 'rockstar.apps.blog.xmlrpc.rpc_handler'),
    (r'^edituri/rsd.xml$', 'rockstar.apps.blog.xmlrpc.edituri'),

    # Django RSS
    # The following two are for backwards compatibility.
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),

    (r'^comments/', include('django.contrib.comments.urls.comments')),

    (r'^all/', 'django.views.generic.date_based.archive_index',
        {'template_name': 'index.html',
            'queryset': Post.objects.all(), 'date_field': 'post_date'}),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    (r'^$', 'django.views.generic.date_based.archive_index',
        dict(info_dict, template_name='index.html', num_latest=10)),
)
