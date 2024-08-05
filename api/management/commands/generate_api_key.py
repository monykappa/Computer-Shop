
from django.core.management.base import BaseCommand
from api.models import APIKey

class Command(BaseCommand):
    help = 'Generate a new API key'

    def handle(self, *args, **kwargs):
        api_key = APIKey.objects.create()
        self.stdout.write(self.style.SUCCESS(f'Generated API Key: {api_key.key}'))
