from django.db.models import Count
from ..business import common
from ..models import Category


def get_categories():
    return Category.objects().order_by("name")


def create_if_not_exists(categories):
    for category in categories:
        category.save()


def get_categories_frequency():
    query_set = Category.objects.annotate(posts_count=Count('post')) \
        .order_by('-posts_count') \
        .values('name', 'posts_count')
    return common.query_set_to_dict('name', 'posts_count', query_set)
