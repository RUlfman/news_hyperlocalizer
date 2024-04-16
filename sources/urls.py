from django.urls import path
from sources import views


urlpatterns = [
    path('', views.source_index, name='source_index'),
    path('<int:pk>/', views.source_detail, name='source_detail'),
    path('api/sources/', views.SourceListCreate.as_view(), name='source-list-create'),
    path('api/sources/<int:pk>/', views.SourceRetrieveUpdateDestroy.as_view(), name='source-detail'),
]