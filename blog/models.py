from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    date = models.DateField()
    checksum = models.SlugField(max_length=256)
    categories = models.CharField(max_length=256)
    tags = models.CharField(max_length=256)
