from django.urls import path, re_path

from . import views

app_name = "health"
urlpatterns = [
    path('', views.index, name='index'),
]
