from algoliasearch_django import reindex_all
from django.core.management.base import BaseCommand
from properties.models import Property, PropertyImage  # Import the Property model


class Command(BaseCommand):
    help = "Push Property model data to Algolia"

    def handle(self, *args, **kwargs):
        # Reindex the Property model
        reindex_all(PropertyImage)
        self.stdout.write(
            self.style.SUCCESS("Successfully pushed Property data to Algolia!")
        )
