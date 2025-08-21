# accounts/management/commands/create_admin_superuser.py
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

        # Check if user exists
        if not User.objects.filter(username=username).exists():
            # Explicitly set role='admin'
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role='admin',
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" with role "admin" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))

