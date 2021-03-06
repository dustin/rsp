from django.db import models
from django.contrib import admin

FORMATS=(
    (1, 'html'),
    (2, 'markdown')
    )

class Tag(models.Model):

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    class Admin:
        pass

class Post(models.Model):

    post_date=models.DateTimeField('date posted')
    title=models.CharField(max_length=128)
    slug=models.CharField(max_length=128)
    tags=models.ManyToManyField(Tag)
    released=models.BooleanField()
    contents=models.TextField()
    format=models.IntegerField(choices=FORMATS, default=1)

    def get_full_path(self):
        return '%s/%s/' % \
            (self.post_date.strftime("%Y/%b/%d").lower(), self.slug)

    def get_absolute_url(self):
        return '/post/' + self.get_full_path()

    def __str__(self):
        return self.title + " on " + self.post_date.ctime()

    class Meta:
        ordering = ['-post_date', '-id']

class PostAdmin(admin.ModelAdmin):
    search_fields=('title', 'contents',)
    list_filter=('post_date', 'released',)
    list_display=('post_date', 'title', 'slug', 'released',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)

