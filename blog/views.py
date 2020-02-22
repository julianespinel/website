from .models import Post
from .business import markdown_to_html as business
from django.shortcuts import render

import logging


def index(request):
    posts = business.get_posts()
    context = {'posts': posts}
    return render(request, 'blog/index.html', context)


def get_post(request, slug):
    post_path = f'blog/posts/{slug}.html'
    return render(request, post_path)
