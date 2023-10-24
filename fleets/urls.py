from django.urls import path
from .views import FleetListView, FleetDetailView

urlpatterns = [
    path('fleets/', FleetListView.as_view(), name='fleet-list'),
    path('fleets/<int:pk>/', FleetDetailView.as_view(), name='fleet-detail'),
]
