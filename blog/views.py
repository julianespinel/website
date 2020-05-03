from django.shortcuts import render, redirect

from .business import markdown_to_html as business


def index(request):
    posts = business.get_posts()
    categories = business.get_categories_frequency(posts)
    tags = business.get_tags_frequency(posts)
    context = {'posts': posts, 'categories': categories,
               'tags': tags }
    return render(request, 'blog/index.html', context)


def redirect_to_index(request):
    return redirect('blog:index')


def get_post(request, slug):
    post_path = f'blog/posts/{slug}.html'
    context = { 'slug': slug }
    return render(request, post_path, context)


def get_category(request, category):
    template = 'blog/category.html'
    posts = business.get_by_category(category)
    context = { 'category': category, 'posts': posts }
    return render(request, template, context)


def get_tag(request, tag):
    template = 'blog/tag.html'
    posts = business.get_by_tag(tag)
    context = { 'tag': tag, 'posts': posts }
    return render(request, template, context)
