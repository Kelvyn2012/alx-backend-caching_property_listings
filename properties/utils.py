from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Check if properties are in cache
    properties = cache.get('all_properties')
    
    if not properties:
        # Fetch from database if not in cache
        properties = list(Property.objects.all().values())  # convert to list of dicts
        # Store in Redis for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    
    return properties
