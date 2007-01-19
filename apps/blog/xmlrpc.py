#!/usr/bin/env python
"""

Copyright (c) 2005  Dustin Sallings <dustin@spy.net>
"""
# arch-tag: 5900-66-11-0-0030187026

import datetime
import xmlrpclib
import os
import md5
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.sites.models import Site

from rockstar.apps.blog.models import Tag, Post

# Create a Dispatcher; this handles the calls and translates info to function maps
dispatcher = SimpleXMLRPCDispatcher()

def __logError(msg):
    f=open("/tmp/xmlrpc.error", "a")
    f.write(msg)
    f.close()

def edituri(request):
    domain=Site.objects.get_current().domain
    res=render_to_response('rsd.xml', {'domain': domain})
    res.headers['Content-Type']='application/rsd+xml'
    return res

def rpc_handler(request):
    """
    the actual handler:
    if you setup your urls.py properly, all calls to the xml-rpc service
    should be routed through here.
    If post data is defined, it assumes it's XML-RPC and tries to process as such
    Empty post assumes you're viewing from a browser and tells you about the service.
    """
    
    response = HttpResponse()
    if len(request.POST):
        try:
            res=dispatcher._marshaled_dispatch(request.raw_post_data)
        except:
            import traceback
            __logError("input [%s]\n%s\n" \
                % (request.raw_post_data, traceback.format_exc()))
            raise
        response.write(res)
    else:
        response.write("<b>This is an XML-RPC Service.</b><br>")
        response.write("You need to invoke it using an XML-RPC Client!<br>")
        response.write("The following methods are available:<ul>")
        methods = dispatcher.system_listMethods()
        
        for method in methods:
            # right now, my version of SimpleXMLRPCDispatcher always
            # returns "signatures not supported"... :(
            # but, in an ideal world it will tell users what args are expected
            # sig = dispatcher.system_methodSignature(method)
            
            # this just reads your docblock, so fill it in!
            help =  dispatcher.system_methodHelp(method)
            
            response.write("<li><b>%s</b>: %s" % (method, help))
        
        response.write("</ul>")
        response.write('<a href="http://www.djangoproject.com/"><img src="http://media.djangoproject.com/img/badges/djangomade124x25_grey.gif" border="0" alt="Made with Django." title="Made with Django."></a>')
    
    response['Content-length'] = str(len(response.content))
    return response

def multiply(a, b):
    """XML-RPC test.  Multiply two numbers"""
    return a * b

def __doAuth(username, password):
    user=authenticate(username=username, password=password)
    if user is None:
        raise "Authentication failed"
    return user

def __postToStruct(post):
    rv={}
    rv['postid']=post.id
    rv['title']=post.title
    rv['link']=post.slug
    rv['dateCreated']=xmlrpclib.DateTime(post.post_date.timetuple())
    rv['description']=post.contents
    rv['categories']=[t.name for t in post.tags.all()]
    rv['mt_allow_comments']=post.comments_allowed
    return rv

def __lookupTags(struct):
    rv=[]
    if 'categories' in struct:
        for t in struct['categories']:
            rv.append(Tag.objects.get(name__exact=t))
    return rv

def __slugify(title):
    import sre
    import sets
    rm=sets.Set(("", "a", "an", "as", "at", "before", "but", "by", "for",
        "from", "is", "in", "into", "like", "of", "off", "on", "onto", "per",
        "since", "than", "the", "this", "that", "to", "up", "via", "with"))
    cleaned=sre.sub("[^\w\s]", "", title).lower()
    rv='-'.join([x for x in sre.split("[\W]", cleaned) if x not in rm])
    return rv

def __getSlug(struct):
    return struct.get('link', __slugify(struct['title']))

def __areCommentsAllowed(struct):
    return (struct.get('mt_allow_comments', 1) == 1)

def __recentPosts(num):
    return Post.objects.all()[:num]

def newPost(blogid, username, password, struct, publish):
    """Post a new entry, return the post ID"""
    __doAuth(username, password)
    post=Post(post_date=datetime.datetime.now(),
        title=struct['title'], slug=__getSlug(struct), released=publish)

    # Stupid del.icio.us was sending the contents as a base64 blob
    c=struct['description']
    if isinstance(c, xmlrpclib.Binary):
        c=c.data
    post.contents=c

    post.comments_allowed=__areCommentsAllowed(struct)
    # Have to save it before applying tags so the relationship exists
    post.save()
    post.tags=__lookupTags(struct)
    post.save()
    return post.id

def getRecentPosts(blogid, username, password, num):
    """Get the recent posts in the given blog."""
    __doAuth(username, password)
    return [__postToStruct(x) for x in __recentPosts(num)]

def editPost(postid, username, password, struct, publish):
    """Edit a post"""
    __doAuth(username, password)
    post=Post.objects.get(pk=int(postid))
    post.title=struct['title']
    post.link=__getSlug(struct)
    post.contents=struct['description']
    post.tags=__lookupTags(struct)
    post.released=publish
    post.comments_allowed=__areCommentsAllowed(struct)
    post.save()
    return True

def getPost(postid, username, password):
    """Get a post"""
    __doAuth(username, password)
    post=Post.objects.get(pk=int(postid))
    return __postToStruct(post)

def deletePost(garbage, postid, username, password, publish):
    """Delete a post"""
    __doAuth(username, password)
    Post.objects.get(pk=int(postid)).delete()
    return True

def getCategories(blogid, username, password):
    """Get all known categories"""
    __doAuth(username, password)
    rv={}
    for t in Tag.objects.all():
        rv[t.name]={'description': t.name,
            'htmlUrl': '', 'rssUrl': ''}
    return rv

def getUsersBlogs(garbage, username, password):
    """Get the blogs available to the given user"""
    user=__doAuth(username, password)
    rv=[]
    domain=Site.objects.get_current().domain
    rv.append({'blogid': "1", 'blogName': "Rockstar Programmer",
        'url': 'http://%s/' % (domain,)})
    return rv

def getRecentPostTitles(blogid, username, password, num):
    """Get the titles of the recent post in this blog."""
    __doAuth(username, password)
    rv=[]
    for post in __recentPosts(num):
        rv.append({
            'dateCreated': xmlrpclib.DateTime(post.post_date.timetuple()),
            'userid': username, 'postid': post.id, 'title': post.title})
    return rv

def getPostCategories(postid, username, password):
    """Get the categories for the given post."""
    __doAuth(username, password)
    post=Post.objects.get(pk=int(postid))
    rv=[]
    for t in post.tags.all():
        rv.append({'categoryName': t.name, 'categoryId': t.id,
            'isPrimary': False})
    return rv

def setPostCategories(postid, username, password, cats):
    """Set the categories for a post."""
    __doAuth(username, password)
    post=Post.objects.get(pk=int(postid))
    post.tags=[Tag.objects.get(name__exact=t['categoryId']) for t in cats]
    post.save()
    return True

def supportedMethods():
    """Get the list of supported methods."""
    return dispatcher.system_listMethods()

def publishPost(postid, username, password):
    """Publish a post."""
    __doAuth(username, password)
    post=Post.objects.get(pk=int(postid))
    post.released=True
    post.save()
    return True

def getCategoryList(blogid, username, password):
    """Get all known categories (MT style)"""
    __doAuth(username, password)
    rv=[]
    for t in Tag.objects.all():
        rv.append({'categoryId': t.name, 'categoryName': t.name})
    return rv

def newMediaObject(blogid, username, password, struct):
    __doAuth(username, password)
    extensions={'image/jpeg': 'jpg', 'image/gif': 'gif', 'image/png': 'png',
        'video/quicktime': 'mov', 'audio/mp3': 'mp3', 'audio/mpeg': 'mp3'}
    ext=extensions.get(struct['type'])
    if ext is None:
        raise "Unsupported type:  " + struct['type']

    bits=struct['bits'].data
    assert len(bits) > 0
    m=md5.new(bits).hexdigest()
    fn=os.path.join(m[:2], m + "." + ext)

    uploc=settings.MEDIA_ROOT
    uplochashed=os.path.join(uploc, m[:2])
    filename=os.path.join(uploc, fn)
    if not os.path.exists(filename):
        if not os.path.exists(uplochashed):
            os.makedirs(uplochashed)
        f=open(filename, "w")
        try:
            f.write(bits)
        finally:
            f.close()

    url = settings.MEDIA_URL + "/" + fn

    rv={'url': url}
    return rv

dispatcher.register_function(multiply, "test.multiply")
dispatcher.register_function(newPost, "metaWeblog.newPost")
dispatcher.register_function(editPost, "metaWeblog.editPost")
dispatcher.register_function(getPost, "metaWeblog.getPost")
dispatcher.register_function(getCategories, "metaWeblog.getCategories")
dispatcher.register_function(getRecentPosts, "metaWeblog.getRecentPosts")
dispatcher.register_function(deletePost, "metaWeblog.deletePost")
dispatcher.register_function(newMediaObject, "metaWeblog.newMediaObject")
# Compatibility with blogger, since this is what MarsEdit wants.
dispatcher.register_function(deletePost, "blogger.deletePost")
dispatcher.register_function(getUsersBlogs, "blogger.getUsersBlogs")

# moveable type support
dispatcher.register_function(getRecentPostTitles, "mt.getRecentPostTitles")
dispatcher.register_function(getCategoryList, "mt.getCategoryList")
dispatcher.register_function(getPostCategories, "mt.getPostCategories")
dispatcher.register_function(setPostCategories, "mt.setPostCategories")
dispatcher.register_function(supportedMethods, "mt.supportedMethods")
dispatcher.register_function(publishPost, "mt.publishPost")
