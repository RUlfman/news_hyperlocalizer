from django.urls import path
from stories import views


urlpatterns = [
    path('', views.story_index, name='story_index'),
    path('<int:pk>/', views.story_detail, name='story_detail'),
    path('labels/', views.label_index, name='label_index'),
]
