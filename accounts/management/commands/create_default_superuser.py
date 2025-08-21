from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

class Command(BaseCommand):
    help = 'Create a default superuser with role admin if it does not exist'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = getattr(settings, 'DJANGO_SUPERUSER_USERNAME', 'admin')
        email = getattr(settings, 'DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = getattr(settings, 'DJANGO_SUPERUSER_PASSWORD', 'admin')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
