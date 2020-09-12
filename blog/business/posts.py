from ..models import Post
from ..business import markdown_to_html

from django.conf import settings


def get_posts():
    if settings.DEBUG:
        markdown_to_html.refresh_posts()
    return Post.objects.order_by('-date')


def get_by_category(category):
    return Post.objects.filter(categories__contains=[category]).order_by('-date')


def get_by_tag(tag):
    return Post.objects.filter(tags__contains=[tag]).order_by('-date')


def sort_dictionary_desc(categories_frequency):
    tuples = list(categories_frequency.items())
    sorted_tuples = sorted(tuples, key=lambda pair: pair[1], reverse=True)
    return dict(sorted_tuples)


def get_categories_frequency(posts):
    categories_frequency = {}
    for post in posts:
        categories = post.categories
        for category in categories:
            occurrences = categories_frequency.get(category, 0)
            categories_frequency[category] = occurrences + 1
    return sort_dictionary_desc(categories_frequency)


def get_tags_frequency(posts):
    tags_frequency = {}
    for post in posts:
        tags = post.tags
        for tag in tags:
            occurrences = tags_frequency.get(tag, 0)
            tags_frequency[tag] = occurrences + 1
    return sort_dictionary_desc(tags_frequency)
