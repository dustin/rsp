from django.db import models

class Tag(models.Model):

    name = models.CharField(maxlength=32)

    def __str__(self):
        return self.name

    class Admin:
        ordering = ['name']

class Post(models.Model):

    post_date=models.DateTimeField('date posted')
    title=models.CharField(maxlength=128)
    slug=models.SlugField(prepopulate_from=['title'])
    tags=models.ManyToManyField(Tag)
    released=models.BooleanField()
    contents=models.TextField()

    def get_full_path(self):
        return '%s/%s' % \
            (self.post_date.strftime("%Y/%b/%d").lower(), self.slug)

    def get_absolute_url(self):
        return '/post/' + self.get_full_path()

    def __str__(self):
        return self.title + " on " + self.post_date.ctime()

    class Admin:

        ordering = ['-post_date', '-id']
        search_fields=('title', 'contents',)
        list_filter=('post_date', 'released',)
        list_display=('post_date', 'title', 'slug', 'released',)

