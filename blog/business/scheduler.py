import logging
from ..models import Post
from apscheduler.schedulers.background import BackgroundScheduler
from .markdown_to_html import refresh_posts


def schedule_posts_refresh():
    scheduler = BackgroundScheduler()
    scheduler.add_job(refresh_posts, 'interval', minutes=3)
    scheduler.start()
