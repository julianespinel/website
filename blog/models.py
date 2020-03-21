from django.db import models
from django.contrib.postgres.fields import ArrayField

class Post(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    date = models.DateField()
    checksum = models.SlugField(max_length=256)
    categories = ArrayField(models.CharField(max_length=32))
    tags = ArrayField(models.CharField(max_length=32))
