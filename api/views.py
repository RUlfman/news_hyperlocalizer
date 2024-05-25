from rest_framework import generics, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Source

from story_collection.collection import collect_stories_from_source
from .serializers import *

# Helper function to filter queryset based on query parameters
def filter_queryset(queryset, query_params, fields, min_value_fields):
    for field, field_type in fields.items():
        value = query_params.get(field, None)
        if value is not None:
            if field_type == 'int':
                value = int(value)
                if field in min_value_fields:
                    queryset = queryset.filter(**{f"{field}__gte": value})
                else:
                    queryset = queryset.filter(**{f"{field}": value})
            elif field_type == 'string':
                if field == 'label':
                    queryset = queryset.filter(labels__name__icontains=value)
                else:
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
        return filter_queryset(queryset, self.request.query_params, fields, [])


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
        openapi.Parameter('created', openapi.IN_QUERY, description="Date the story was created", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('updated', openapi.IN_QUERY, description="Date the story was updated", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('needsKnow', openapi.IN_QUERY, description="Minimum 'Know' userneed of the story", type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter('needsUnderstand', openapi.IN_QUERY, description="Minimum 'Understand' userneed of the story", type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter('needsFeel', openapi.IN_QUERY, description="Minimum 'Feel' userneed of the story", type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter('needsDo', openapi.IN_QUERY, description="Minimum 'Do' userneed of the story", type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter('needsSum', openapi.IN_QUERY, description="Minimum Sum of userneeds of the story", type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter('label', openapi.IN_QUERY, description="Label of the story", type=openapi.TYPE_STRING, required=False),
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
            'updated': 'date',
            'needsKnow': 'int',
            'needsUnderstand': 'int',
            'needsFeel': 'int',
            'needsDo': 'int',
            'needsSum': 'int',
            'label': 'string',
        }
        min_value_fields = ['needsKnow', 'needsUnderstand', 'needsFeel', 'needsDo', 'needsSum']
        return filter_queryset(queryset, self.request.query_params, fields, min_value_fields)

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
        return filter_queryset(queryset, self.request.query_params, fields, [])


class LabelRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]


from rest_framework.decorators import api_view

@csrf_exempt
@swagger_auto_schema(
    method='post',
    operation_description="Collect stories from a specific source",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'sourceid': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the source'),
        },
        required=['sourceid'],
    ),
    responses={200: openapi.Response(description="Stories collected successfully")}
)
@api_view(['POST'])
def collect_stories(request):
    if request.method == 'POST':
        source_id = request.data.get('sourceid')
        if not source_id:
            return HttpResponseBadRequest("sourceid is required")
        try:
            source = Source.objects.get(id=source_id)
        except Source.DoesNotExist:
            return HttpResponseBadRequest("No Source object found with ID {}".format(source_id))
        collect_stories_from_source(source)
        return JsonResponse({"message": "Stories collected successfully"})
    else:
        return HttpResponseBadRequest("Invalid HTTP method")