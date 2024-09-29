from django.urls import path
from .views import AddProblemView

urlpatterns = [
    path('add_problem/', AddProblemView.as_view(), name='add_problem'),
    # Add other URL patterns for your app here
]