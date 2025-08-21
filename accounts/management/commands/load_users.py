import os
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Load users from fixtures/users.json"

    def handle(self, *args, **kwargs):
        fixture_path = os.path.join(os.path.dirname(__file__), '..', '..', 'fixtures', 'users.json')
        fixture_path = os.path.abspath(fixture_path)
        if os.path.exists(fixture_path):
            call_command('loaddata', fixture_path)
            self.stdout.write(self.style.SUCCESS("Users loaded successfully."))
        else:
            self.stdout.write(self.style.ERROR(f"Fixture file not found at {fixture_path}"))

