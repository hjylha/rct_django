
from django.urls import path

from .views import product_table_view

app_name = 'stalls'
urlpatterns = [
    path('', product_table_view, name='product-table')
]