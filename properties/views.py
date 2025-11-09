from django.shortcuts import render
from .models import Property
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from .utils import get_all_properties
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all properties. Results are cached for 15 minutes.",
    responses={
        200: openapi.Response(
            description="List of properties",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'properties': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT),
                        description="Array of property objects"
                    )
                }
            )
        )
    },
    tags=['Properties']
)
@api_view(['GET'])
@cache_page(60 * 15)
def property_list(request):
    """
    View to return all properties as json.
    """
    data = get_all_properties()
    return JsonResponse({'properties': data})
