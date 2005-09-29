from django.core import rss
from django.models.core import sites
from django.models.comments import freecomments

# these are entries of my blog
from django.models.blog import posts

blog_full_feed = rss.FeedConfiguration(
    slug = 'full',
    title_cb = lambda param: "Noelani's Blog",
    link_cb = lambda param: 'http://%s/' % sites.get_current().domain,
    description_cb = lambda param: "Stuff that's on Noelani's mind",
    get_list_func_cb = lambda param: posts.get_list,
    get_list_kwargs = {
        'released__exact': True,
        'limit': 10,
        'order_by': ['-post_date', '-id']
    }
)

blog_summary_feed = rss.FeedConfiguration(
    slug = 'summary',
    title_cb = lambda param: "Noelani's Blog",
    link_cb = lambda param: 'http://%s/' % sites.get_current().domain,
    description_cb = lambda param: "Stuff that's on Noelani's mind",
    get_list_func_cb = lambda param: posts.get_list,
    get_list_kwargs = {
        'released__exact': True,
        'limit': 10,
        'order_by': ['-post_date', '-id']
    }
)

blog_comments_feed = rss.FeedConfiguration(
    slug = 'comments',
    title_cb = lambda param: "Noelani's Recent Comments",
    link_cb = lambda param: 'http://%s/' % sites.get_current().domain,
    description_cb = lambda param: "Recent comments on posts in Noelani's blog.",
    get_list_func_cb = lambda param: freecomments.get_list,
    get_list_kwargs = {
        'limit': 20,
    }
)

rss.register_feed(blog_full_feed)
rss.register_feed(blog_summary_feed)
rss.register_feed(blog_comments_feed)
