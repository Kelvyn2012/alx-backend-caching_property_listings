from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    # Check if properties are in cache
    properties = cache.get('all_properties')
    
    if not properties:
        # Fetch from database if not in cache
        properties = list(Property.objects.all().values())  # convert to list of dicts
        # Store in Redis for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    
    return properties




def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    Logs the metrics and returns them as a dictionary.
    """
    redis_conn = get_redis_connection("default")
    info = redis_conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    # Calculate hit ratio using a formula without conditional
    hit_ratio = hits / (hits + misses) if (hits + misses) else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2)
    }

    # Log metrics (not using logger.error)
    logger.info(f"Redis Cache Metrics: {metrics}")

    return metrics