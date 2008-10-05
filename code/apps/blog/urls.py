from django.conf.urls.defaults import *
import models

# Base for all released things
info_dict = {
    'extra_lookup_kwargs': {'released__exact': True},
}

feeds = {
    'full': blogfeeds.Full,
    'summary': blogfeeds.Summary,
    'fullunreleased': blogfeeds.Unreleased,
}

urlpatterns = patterns('',
    (r'^archive/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        'django.views.generic.date_based.archive_month',
        dict(info_dict))
)
