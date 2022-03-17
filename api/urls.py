from django.urls import path
from .views import OverviewAPI, get_ridenames, get_products

urlpatterns = [
    path('', OverviewAPI),
    path('ridetypes/', get_ridenames),
    path('products/', get_products)
]