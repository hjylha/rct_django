from django.urls import path
from .views import ride_add_view, calculator_view

urlpatterns = [
    path('', calculator_view, name='calculator'),
    path('add/', ride_add_view, name='add-ride')
]
