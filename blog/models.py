from django.db import models


class Category(models.Model):
    name = models.SlugField(max_length=32, primary_key=True)


class Tag(models.Model):
    name = models.SlugField(max_length=32, primary_key=True)


class Post(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)
    date = models.DateField()
    checksum = models.SlugField(max_length=256)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
