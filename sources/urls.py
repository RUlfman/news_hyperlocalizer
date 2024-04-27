from django.urls import path
from sources import views


urlpatterns = [
    path('', views.source_index, name='source_index'),
    path('<int:pk>/', views.source_detail, name='source_detail'),
]