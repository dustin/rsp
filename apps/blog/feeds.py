#!/usr/bin/env python
"""

Copyright (c) 2005  Dustin Sallings <dustin@spy.net>
"""

from django.contrib.syndication.feeds import Feed
from django.models.comments import freecomments
from django.contrib.comments import feeds
from django.models.blog import posts

class Full(Feed):
    title = "Noelani's Blog - Full Posts"
    link = "/"
    description = "Stuff that's on Noelani's mind"

    author_name = 'Noelani Sallings'

    author_email = 'noelani@spy.net'

    author_link = 'http://bleu.west.spy.net/~noelani/'

    def item_pubdate(self, item):
        return item.post_date
    
    def items(self):
        return posts.get_list(released__exact=True,
            order_by=('-post_date', '-id'), limit=10)

class Summary(Full):
    title = "Noelani's Blog - Post Summaries"

class Unreleased(Full):
    title = "Noelani's Blog - Unreleased"
    
    def items(self):
        return posts.get_list(order_by=('-post_date', '-id'), limit=10)

class Comments(feeds.LatestFreeCommentsFeed):
    title = "Noelani's Recent Comments"
    description = "Recent comments on Noelani's blog"
