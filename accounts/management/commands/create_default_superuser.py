from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Create a default superuser and load users from fixture'

    def handle(self, *args, **kwargs):
        # Step 1: Create default superuser if it does not exist
        User = get_user_model()
        username = getattr(settings, 'DJANGO_SUPERUSER_USERNAME', 'admin')
        email = getattr(settings, 'DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = getattr(settings, 'DJANGO_SUPERUSER_PASSWORD', 'admin')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))

        # Step 2: Load users from fixture
        fixture_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'fixtures', 'users.json')
        if os.path.exists(fixture_path):
            call_command('loaddata', fixture_path)
            self.stdout.write(self.style.SUCCESS("Users loaded successfully from users.json."))
        else:
            self.stdout.write(self.style.WARNING(f"Fixture file not found at {fixture_path}"))


