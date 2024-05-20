from django.urls import path
from pages import views
from mock import views as mock_views
from story_evaluation import views as evaluation_views


urlpatterns = [
    path("", views.home, name='home'),
    path('clear_data/', mock_views.clear_data_view, name='clear_data'),
    path('populate_sources/', mock_views.populate_sources_view, name='populate_sources'),
    path('populate_stories/', mock_views.populate_stories_view, name='populate_stories'),
    path('assign_random_labels/', mock_views.assign_random_labels_view, name='assign_random_labels'),
    path('evaluate_userneeds/', evaluation_views.evaluate_userneeds_view, name='evaluate_userneeds'),
]
