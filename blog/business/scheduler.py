import logging
from ..models import Post
from apscheduler.schedulers.background import BackgroundScheduler
from .markdown_to_html import get_new_and_updated


logger = logging.getLogger(__name__)


def schedule_posts_refresh():
    scheduler = BackgroundScheduler()
    scheduler.add_job(__convert_posts_to_html, 'interval', minutes=3)
    scheduler.start()


def __convert_posts_to_html():
    logging.info('Convert posts to html start')
    posts = Post.objects.order_by('-date')
    (new_posts, updated_posts) = get_new_and_updated(posts)
    logger.info(f'new_posts: {new_porsts}')
    logger.info(f'updated_posts: {updated_posts}')
    Post.objects.bulk_create(new_posts)
    Post.objects.bulk_update(updated_posts, ['checksum'])
    logging.info('Convert posts to html end')
