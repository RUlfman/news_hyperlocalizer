from django.urls import path
from pages import views
from mock import views as mock_views
from ai_evaluation import views as ai_evaluation_views


urlpatterns = [
    path("", views.home, name='home'),
    path('populate_mock_data/', mock_views.populate_mock_data_view, name='populate_mock_data'),
    path('evaluate_userneeds/', ai_evaluation_views.evaluate_userneeds_view, name='evaluate_userneeds'),
]
