from ..models import Post, Category
from ..business import markdown_to_html
from ..business import categories, tags

from django.conf import settings


def get_posts():
    if settings.DEBUG:
        markdown_to_html.refresh_posts()
    return Post.objects.order_by('-date')


def get_by_category(category):
    return Post.objects.filter(categories__name=category).order_by('-date')


def get_by_tag(tag):
    return Post.objects.filter(tags__name=tag).order_by('-date')


def create(post, post_categories, post_tags):
    categories.create_if_not_exists(post_categories)
    tags.create_if_not_exists(post_tags)
    post.save()
    post.categories.add(*post_categories)
    post.tags.add(*post_tags)


def delete_all():
    Post.objects.all().delete()
