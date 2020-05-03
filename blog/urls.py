from django.urls import path, re_path

from . import views

app_name = "blog"
urlpatterns = [
    path('', views.index, name='index'),

    re_path(r'posts/?$', views.redirect_to_index),
    re_path(r'categories/?$', views.redirect_to_index),
    re_path(r'tags/?$', views.redirect_to_index),

    path('posts/<slug:slug>', views.get_post, name='post'),
    path('categories/<slug:category>', views.get_category, name='category'),
    path('tags/<slug:tag>', views.get_tag, name='tag')
]
