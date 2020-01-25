from django.shortcuts import render

import logging

# Create your views here.
def index(request):
    # return HttpResponse('Hello world')
    return render(request, 'blog/index.html')

def get_post(request, slug):
    post_path = f'blog/posts/{slug}.html'
    return render(request, post_path)
