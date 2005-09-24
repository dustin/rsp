from django.core import meta

# Create your models here.

class Tag(meta.Model):

    name=meta.CharField(maxlength=32)

    class META:
        admin = meta.Admin()

        ordering = ['name']

    def __repr__(self):
        return self.name

class Post(meta.Model):

    post_date=meta.DateTimeField('date posted')
    title=meta.CharField(maxlength=128)
    slug=meta.SlugField(prepopulate_from=['title'])
    tags=meta.ManyToManyField(Tag, blank=True, null=True)
    released=meta.BooleanField()
    contents=meta.TextField()

    def get_full_path(self):
        return '%s/%s/' % \
            (self.post_date.strftime("%Y/%b/%d").lower(), self.slug)

    def get_absolute_url(self):
        return '/post/' + self.get_full_path()

    class META:
        ordering = ['-post_date']

        admin = meta.Admin(
            search_fields=('title', 'contents',),
            list_filter=('post_date', 'released',),
            list_display=('post_date', 'title', 'slug', 'released',)
            )

    def __repr__(self):
        return self.title + " on " + self.post_date.ctime()
