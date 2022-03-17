
from django.urls import path

from .views import ridetype_overview_view, individual_ridetype_view

app_name = 'ridetypes'
urlpatterns = [
    path('', ridetype_overview_view, name='ridetype-table'),
    path('<str:name>', individual_ridetype_view, name='ridetype-detail')
]
