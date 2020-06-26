from django.core.management.base import BaseCommand
from blog.business import markdown_to_html


class Command(BaseCommand):
    help = 'Convert posts written in markdown to html'

    def handle(self, *args, **options):
        markdown_to_html.refresh_posts()
        self.stdout.write(self.style.SUCCESS('HTML files created'))
