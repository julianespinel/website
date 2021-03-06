from django.shortcuts import render, redirect

from .business import posts, categories, tags
from .business import markdown_to_html


def index(request):
    posts_from_db = posts.get_posts()
    categories_frequency = categories.get_categories_frequency()
    tags_frequency = tags.get_tags_frequency()
    context = {'posts': posts_from_db,
               'categories': categories_frequency,
               'tags': tags_frequency}
    return render(request, 'blog/index.html', context)


def redirect_to_index(request):
    return redirect('blog:index')


def get_post(request, slug):
    post_path = f'blog/posts/{slug}.html'
    context = {'slug': slug}
    return render(request, post_path, context)


def get_category(request, category):
    template = 'blog/category.html'
    posts_from_db = posts.get_by_category(category)
    context = {'category': category, 'posts': posts_from_db}
    return render(request, template, context)


def get_tag(request, tag):
    template = 'blog/tag.html'
    posts_from_db = posts.get_by_tag(tag)
    context = {'tag': tag, 'posts': posts_from_db}
    return render(request, template, context)


def refresh_posts(request):
    markdown_to_html.refresh_posts()
    return redirect('blog:index')
