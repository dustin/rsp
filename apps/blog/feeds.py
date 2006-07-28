#!/usr/bin/env python
"""

Copyright (c) 2005  Dustin Sallings <dustin@spy.net>
"""

from django.contrib.syndication.feeds import Feed
from django.models.comments import freecomments
from django.contrib.comments import feeds
from django.models.blog import posts

class Full(Feed):
    title = "RockStarProgrammer - Full Posts"
    link = "/"
    description = "Rants of an accidental Rock Star Programmer"

    author_name = 'Dustin Sallings'

    author_email = 'dustin@spy.net'

    author_link = 'http://bleu.west.spy.net/~dustin/'

    def item_pubdate(self, item):
        return item.post_date
    
    def items(self):
        return posts.get_list(released__exact=True,
            order_by=('-post_date', '-id'), limit=10)

class Summary(Full):
    title = "RockStarProgrammer - Post Summaries"

class Unreleased(Full):
    title = "RockStarProgrammer - Unreleased"
    
    def items(self):
        return posts.get_list(order_by=('-post_date', '-id'), limit=10)

class Comments(feeds.LatestFreeCommentsFeed):
    title = "RockStarProgrammer Recent Comments"
    description = "Recent comments at RockStarProgrammer"

    def item_author_name(self, item):
        return item.person_name

    def item_pubdate(self, item):
        return item.submit_date
