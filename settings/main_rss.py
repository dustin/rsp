from django.core import rss
from django.models.core import sites

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

rss.register_feed(blog_full_feed)
rss.register_feed(blog_summary_feed)
