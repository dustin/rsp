from django.db import models

FORMATS=(
    (1, 'html'),
    (2, 'markdown')
    )

class Tag(models.Model):

    name = models.CharField(maxlength=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    class Admin:
        pass

class MimeType(models.Model):
    type = models.CharField(maxlength=64)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ['type']

    class Admin:
        pass

class Post(models.Model):

    post_date=models.DateTimeField('date posted')
    title=models.CharField(maxlength=128)
    slug=models.SlugField(prepopulate_from=['title'])
    tags=models.ManyToManyField(Tag)
    released=models.BooleanField()
    contents=models.TextField()
    format=models.IntegerField(choices=FORMATS, default=1)
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

    class Meta:
        ordering = ['-post_date', '-id']

    class Admin:
        search_fields=('title', 'contents',)
        list_filter=('post_date', 'released',)
        list_display=('post_date', 'title', 'slug', 'released',)

