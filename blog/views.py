from django.shortcuts import render

from .business import markdown_to_html as business


def index(request):
    posts = business.get_posts()
    categories = business.get_categories_frequency(posts)
    tags = business.get_tags_frequency(posts)
    context = {'posts': posts, 'categories': categories,
               'tags': tags }
    return render(request, 'blog/index.html', context)


def get_post(request, slug):
    post_path = f'blog/posts/{slug}.html'
    context = { 'slug': slug }
    return render(request, post_path, context)
