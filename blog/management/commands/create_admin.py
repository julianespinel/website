from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

email = settings.DEFAULT_ADMIN_EMAIL
username = settings.DEFAULT_ADMIN_USERNAME
password = settings.DEFAULT_ADMIN_PASSWORD

class Command(BaseCommand):
    """
    How to run?
    python manage.py create_admin --settings=settings.local
    """
    help = "Create a default admin if there are no admins"

    def handle(self, *args, **options):
        admins = User.objects.filter(is_superuser=True, is_active=True)
        if len(admins) > 0:
            self.stdout.write(self.style.SUCCESS('Default admin already exists'))
            return

        User.objects.create_user(
            email=email,
            username=username,
            password=password,
            is_staff=True,
            is_active=True,
            is_superuser=True
        )
        self.stdout.write(self.style.SUCCESS('Default admin was created'))
