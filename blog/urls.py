from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<slug:slug>', views.get_post, name='post'),
    path('categories/<slug:category>', views.get_category, name='category'),
    path('tags/<slug:tag>', views.get_tag, name='tag')
]
