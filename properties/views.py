from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties

@cache_page(60 * 15)   # 15 minutes
def property_list(request):
    properties = get_all_properties()  # use cached data
    return JsonResponse({"data": properties})