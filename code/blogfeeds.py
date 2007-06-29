#!/usr/bin/env python
"""

Copyright (c) 2005  Dustin Sallings <dustin@spy.net>
"""

from django.contrib.syndication.feeds import Feed
from django.contrib.comments.feeds import LatestFreeCommentsFeed
from rockstar.apps.blog.models import Post, Tag

class Full(Feed):
    title = "RockStarProgrammer - Full Posts"
    link = "/"
    description = "Rants of an accidental Rock Star Programmer"

    author_name = 'Dustin Sallings'

    author_email = 'dustin@spy.net'

    author_link = 'http://bleu.west.spy.net/~dustin/'

    # Invoked when there's extra URL stuff.
    def get_object(self, bits):
        return Tag.objects.filter(name__in=bits[0].split('+'))

    def item_enclosure_url(self, item):
        return item.enclosure_url

    def item_enclosure_length(self, item):
        return item.enclosure_length

    def item_enclosure_mime_type(self, item):
        return item.enclosure_type.type

    def item_pubdate(self, item):
        return item.post_date
    
    def items(self, obj):
        sel=Post.objects.filter(released__exact=True)
        if obj:
            sel=sel.filter(tags__in=obj)
        return sel.order_by('-post_date', '-id')[:10]

class Summary(Full):
    title = "RockStarProgrammer - Post Summaries"

class Unreleased(Full):
    title = "RockStarProgrammer - Unreleased"
    
    def items(self):
        return Post.objects.order_by('-post_date', '-id')[:10]

class Comments(LatestFreeCommentsFeed):
    title = "RockStarProgrammer Recent Comments"
    description = "Recent comments at RockStarProgrammer"

    def item_author_name(self, item):
        return item.person_name

    def item_pubdate(self, item):
        return item.submit_date
