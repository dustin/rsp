from django.db import models

class Tag(models.Model):

    name = models.CharField(maxlength=32)

    def __str__(self):
        return self.name

    class Admin:
        ordering = ['name']

class MimeType(models.Model):
    type = models.CharField(maxlength=64)

    def __str__(self):
        return self.type

    class Admin:
        ordering = ['type']

class Post(models.Model):

    post_date=models.DateTimeField('date posted')
    title=models.CharField(maxlength=128)
    slug=models.SlugField(prepopulate_from=['title'])
    tags=models.ManyToManyField(Tag)
    released=models.BooleanField()
    comments_allowed=models.BooleanField()
    contents=models.TextField()
    enclosure_url=models.CharField(maxlength=512, blank=True, null=True)
    enclosure_length=models.IntegerField(blank=True, null=True)
    enclosure_type=models.ForeignKey(MimeType, blank=True, null=True)
    enclosure_thumb=models.CharField(maxlength=512, blank=True, null=True)

    def get_full_path(self):
        return '%s/%s/' % \
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

