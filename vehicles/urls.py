from django.urls import path
from .views import VehicleListView, VehicleDetailView, DriverListView, DriverDetailView, LocationListView, LocationDetailView, LatestLocationView, VehicleLocationAssignmentView, unassign_driver_from_vehicle, assign_driver_to_vehicle, FleetVehicleLocationsView

urlpatterns = [
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('drivers/<int:pk>/', DriverDetailView.as_view(), name='driver-detail'),
    path('<int:vehicle_id>/location/', LocationListView.as_view(), name='add-location'),
    path('<int:vehicle_id>/updatelocation/', LocationDetailView.as_view(), name='vehicle-update-location'),
    path('<int:vehicle_id>/last_location/', LatestLocationView.as_view(), name='latest_location'),
    path('unassign/<int:vehicle_id>/', unassign_driver_from_vehicle, name='unassign_driver_from_vehicle'),
    path('assign/<int:vehicle_id>/<int:driver_id>/', assign_driver_to_vehicle, name='assign-driver-to-vehicle'),
    path('<int:vehicle_id>/assign_location/', VehicleLocationAssignmentView.as_view(), name='assign_location'),
    path('fleet/vehicle_locations/', FleetVehicleLocationsView, name='fleet-vehicle-locations'),

]
