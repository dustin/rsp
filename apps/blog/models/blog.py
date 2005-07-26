from django.core import meta

# Create your models here.

class Tag(meta.Model):
    fields = (
        meta.CharField('name', maxlength=32),
    )

    admin = meta.Admin()

    def __repr__(self):
        return self.name

class Post(meta.Model):
    fields = (
        meta.DateTimeField('post_date', 'date posted'),
        meta.CharField('title', maxlength=128),
        meta.ManyToManyField(Tag),
        meta.BooleanField('released'),
        meta.TextField('contents'),
    )

    admin = meta.Admin(
        search_fields=('title', 'contents'),
        list_filter=('post_date', ),
        )

    def __repr__(self):
        return self.title + " on " + self.post_date.ctime()
