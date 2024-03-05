from django.urls import path
from .views import FleetListView, FleetDetailView, VerifyOTPView, SendOTPView, get_user_fleet
from vehicles.views import FleetDriversListView, FleetVehiclesListView, FleetDriversVehiclesListView


urlpatterns = [
    path('fleets/', FleetListView.as_view(), name='fleet-list'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('fleets/<int:fleet_id>/', FleetDetailView.as_view(), name='fleet-detail'),
    path('get_user_fleet/', get_user_fleet, name='get_user_fleet'),
    path('drivers/<int:fleet_id>/', FleetDriversListView.as_view(), name='fleet-drivers-list'),
    path('fleet/vehicles/<int:fleet_id>/', FleetVehiclesListView.as_view(), name='fleet-vehicles-list'),
    path('fleet/drivers-vehicles/<int:fleet_id>/', FleetDriversVehiclesListView.as_view(), name='fleet-drivers-vehicles-list'),

]
