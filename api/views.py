from rest_framework import generics, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime

from .serializers import *


# Helper function to filter queryset based on query parameters
def filter_queryset(queryset, query_params, fields):
    for field, field_type in fields.items():
        value = query_params.get(field, None)
        if value is not None:
            if field_type == 'int':
                value = int(value)
            elif field_type == 'date':
                value = datetime.strptime(value, '%Y-%m-%d').date()
            queryset = queryset.filter(**{f"{field}__icontains": value})
    return queryset


class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = ObtainAuthTokenSerializer
    @swagger_auto_schema(responses={200: ObtainAuthTokenResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SourceListCreate(generics.ListCreateAPIView):
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, description="Name of the source", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('website', openapi.IN_QUERY, description="Website of the source", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('country', openapi.IN_QUERY, description="Country of the source", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('province', openapi.IN_QUERY, description="Province of the source", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('region', openapi.IN_QUERY, description="Region of the source", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('municipality', openapi.IN_QUERY, description="Municipality of the source", type=openapi.TYPE_STRING, required=False)
    ])
    @method_decorator(cache_page(60*15))  # Cache this view for 15 minutes
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Source.objects.all().order_by('name')
        fields = {
            'name': 'string',
            'website': 'string',
            'country': 'string',
            'province': 'string',
            'region': 'string',
            'municipality': 'string'
        }
        return filter_queryset(queryset, self.request.query_params, fields)


class SourceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticated]


class StoryListCreate(generics.ListCreateAPIView):
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, description="Title of the story", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('author', openapi.IN_QUERY, description="Author of the story", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('summary', openapi.IN_QUERY, description="Summary of the story", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('source_id', openapi.IN_QUERY, description="ID of the source", type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter('created', openapi.IN_QUERY, description="Creation date of the story", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False),
        openapi.Parameter('updated', openapi.IN_QUERY, description="Update date of the story", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False)
    ])
    @method_decorator(cache_page(60*15))  # Cache this view for 15 minutes
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Story.objects.all().order_by('-created')
        fields = {
            'title': 'string',
            'author': 'string',
            'summary': 'string',
            'source_id': 'int',
            'created': 'date',
            'updated': 'date'
        }
        return filter_queryset(queryset, self.request.query_params, fields)


class StoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]


class LabelListCreate(generics.ListCreateAPIView):
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, description="Name of the label", type=openapi.TYPE_STRING, required=False),
    ])
    @method_decorator(cache_page(60*15))  # Cache this view for 15 minutes
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Label.objects.all().order_by('name')
        fields = {
            'name': 'string',
        }
        return filter_queryset(queryset, self.request.query_params, fields)


class LabelRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]