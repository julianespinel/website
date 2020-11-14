from django.db.models import Count
from ..business import common
from ..models import Tag


def get_tags():
    return Tag.objects.order_by("name")


def create(tag):
    return Tag.objects.get_or_create(name=tag)


def create_if_not_exists(tags):
    for tag in tags:
        tag.save()


def get_tags_frequency():
    query_set = Tag.objects.annotate(posts_count=Count('post')) \
        .order_by('-posts_count') \
        .values('name', 'posts_count')
    return common.query_set_to_dict('name', 'posts_count', query_set)
