from django.urls import path
from . import views

urlpatterns = [
    path('add_problem/', views.add_problem, name='add_problem'),
    # other paths...
]