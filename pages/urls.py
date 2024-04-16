from django.urls import path
from pages import views
from mock import views as mock_views


urlpatterns = [
    path("", views.home, name='home'),
    path('populate_mock_data/', mock_views.populate_mock_data_view, name='populate_mock_data'),
]
