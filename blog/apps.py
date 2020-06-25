from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        from .business import scheduler
        scheduler.schedule_posts_refresh()
