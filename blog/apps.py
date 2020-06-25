from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        from .business import markdown_to_html
        markdown_to_html.refresh_posts()
