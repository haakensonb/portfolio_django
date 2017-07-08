from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)

class Tag(models.Model):
    tags = models.CharField(max_length=200)

class Post(models.Model):
    title = models.CharField(max_length=50) 
    body = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField('date published')