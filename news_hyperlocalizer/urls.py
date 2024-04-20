from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mock import views as mock_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('stories/', include('stories.urls')),
    path('sources/', include('sources.urls')),
    path('pages/', include('sources.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
