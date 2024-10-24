from django.urls import path, include
from .views import create_recent_submission, get_user_problem_data

urlpatterns = [
    path('recent-submission/', create_recent_submission, name='create_recent_submission'),
    path('user-problem-data/', get_user_problem_data, name='get_user_problem_data'),
    # maybe create two other API endpoints
]
