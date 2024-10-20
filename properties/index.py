import algoliasearch_django as algoliasearch
from .models import Property, PropertyImage  # Import your Property model

# Register the Property model with Algolia
algoliasearch.register(Property)
algoliasearch.register(PropertyImage)
