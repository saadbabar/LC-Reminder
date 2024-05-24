from django.urls import path
from . import views

urlpatterns = [
    path('add_problem/', views.add_problem, name='add_problem'),
    path('get_all_submissions/', views.get_all_submissions, name='get_all_submissions')
    # other paths...
]