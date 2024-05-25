from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import *

schema_view = get_schema_view(
    openapi.Info(
        title="News Hyperlocalizer API",
        default_version="v1",
        description="News Hyperlocalizer API",
        terms_of_service="",
        contact=openapi.Contact(email="r.ulfman@student.fontys.nl"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    path('token/', ObtainTokenPairView.as_view(), name='api-token_obtain_pair'),
    path('sources/', SourceListCreate.as_view(), name='source-list-create'),
    path('sources/<int:pk>/', SourceRetrieveUpdateDestroy.as_view(), name='source-detail'),
    path('stories/', StoryListCreate.as_view(), name='story-list-create'),
    path('stories/<int:pk>/', StoryRetrieveUpdateDestroy.as_view(), name='story-detail'),
    path('labels/', LabelListCreate.as_view(), name='label-list-create'),
    path('labels/<int:pk>/', LabelRetrieveUpdateDestroy.as_view(), name='label-detail'),
    path('collect_stories/', collect_stories, name='collect_stories'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
