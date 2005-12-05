#!/usr/bin/env python
"""

Copyright (c) 2005  Dustin Sallings <dustin@spy.net>
"""

from django.contrib.syndication.feeds import Feed
from django.models.comments import freecomments
from django.models.blog import posts

class Full(Feed):
    title = "Full Posts"
    link = "/"
    description = "Stuff that's on Noelani's mind"
    
    def items(self):
        return posts.get_list(released__exact=True,
            order_by=('-post_date', '-id'), limit=10)

class Summary(Feed):
    title = "Post Summaries"
    link = "/"
    description = "Stuff that's on Noelani's mind"
    
    def items(self):
        return posts.get_list(released__exact=True,
            order_by=('-post_date', '-id'), limit=10)

class Unreleased(Feed):
    title = "Unreleased"
    link = "/"
    description = "Stuff that's on Noelani's mind"
    
    def items(self):
        return posts.get_list(order_by=('-post_date', '-id'), limit=10)

class Comments(Feed):
    title = "Noelani's Recent Comments"
    link = "/"
    description = "Recent comments on Noelani's blog"
    
    def items(self):
        return posts.get_list(order_by=('-post_date', '-id'), limit=20)
