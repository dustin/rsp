#!/usr/bin/env python
"""

Copyright (c) 2005  Dustin Sallings <dustin@spy.net>
"""
# arch-tag: 346-4-119-8187-0030187026

from django.core import template_loader
from django.core.extensions import DjangoContext as Context
from django.models.blog import posts
from django.utils.httpwrappers import HttpResponse

def showRecentReleased(request, tmpl='index', ctype="text/html"):
    post_list = posts.get_list(released__exact = True,
        order_by=['-post_date', '-id'], limit=10)
    t = template_loader.get_template(tmpl)
    c = Context(request, {
        'posts': post_list
    })
    return HttpResponse(t.render(c), ctype)
