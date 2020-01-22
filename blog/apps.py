from django.apps import AppConfig
from blog.business.markdown_to_html import convert_all

import logging

logger = logging.getLogger(__name__)


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        convert_all()
