from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    word = models.CharField(max_length=255)

    def __str__(self):
        return self.word


class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(User, null=True, blank=True)
    # Many different tags can be associated with many different posts
    tags = models.ManyToManyField(Tag, blank=True)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

