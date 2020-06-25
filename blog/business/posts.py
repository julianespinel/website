from ..models import Post


def get_posts():
    return Post.objects.order_by('-date')


def get_by_category(category):
    return Post.objects.filter(categories__contains=[category]).order_by('-date')


def get_by_tag(tag):
    return Post.objects.filter(tags__contains=[tag]).order_by('-date')


def get_categories_frequency(posts):
    categories_frequency = {}
    for post in posts:
        categories = post.categories
        for category in categories:
            occurrences = categories_frequency.get(category, 0)
            categories_frequency[category] = occurrences + 1
    return categories_frequency


def get_tags_frequency(posts):
    tags_frequency = {}
    for post in posts:
        tags = post.tags
        for tag in tags:
            occurrences = tags_frequency.get(tag, 0)
            tags_frequency[tag] = occurrences + 1
    return tags_frequency
