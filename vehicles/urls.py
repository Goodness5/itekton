from django.urls import path
from .views import VehicleListView, VehicleDetailView, DriverListView, DriverDetailView

urlpatterns = [
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('drivers/<int:pk>/', DriverDetailView.as_view(), name='driver-detail'),
    path('<int:pk>/update_location/', VehicleDetailView.as_view(), name='vehicle-update-location'),
]
