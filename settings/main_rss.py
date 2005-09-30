from django.core import rss
from django.models.core import sites
from django.models.comments import freecomments

# these are entries of my blog
from django.models.blog import posts

def formatTime(dt):
    return dt.strftime("%a, %d %Y %H:%M:%S PDT")

# Helper function for making a feed of the posts
def makePostFeed(slug, subtitle, released):
    return rss.FeedConfiguration(
        slug = slug,
        title_cb = lambda param: "Noelani's Blog - " + subtitle,
        link_cb = lambda param: 'http://%s/' % sites.get_current().domain,
        description_cb = lambda param: "Stuff that's on Noelani's mind",
        get_list_func_cb = lambda param: posts.get_list,
        get_pubdate_cb = lambda post: post.post_date,
        get_list_kwargs = {
            'released__exact': released,
            'limit': 10,
        }
    )

blog_comments_feed = rss.FeedConfiguration(
    slug = 'comments',
    title_cb = lambda param: "Noelani's Recent Comments",
    link_cb = lambda param: 'http://%s/' % sites.get_current().domain,
    description_cb = lambda param: "Recent comments on posts in Noelani's blog.",
    get_list_func_cb = lambda param: freecomments.get_list,
    get_pubdate_cb = lambda comment: comment.submit_date,
    get_list_kwargs = {
        'limit': 20,
    }
)

rss.register_feed(makePostFeed('full', "Full Posts", True))
rss.register_feed(makePostFeed('summary', "Post Summaries", True))
rss.register_feed(makePostFeed('fullunreleased', "Unreleased", False))
rss.register_feed(blog_comments_feed)
