from django.core.management.base import BaseCommand
from cms.views import batchGetLiveStatus


class Command(BaseCommand):
    def handle(self, *args, **options):
        batchGetLiveStatus()