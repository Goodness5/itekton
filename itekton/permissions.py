from rest_framework import permissions
from fleets.models import Fleet
from vehicles.models import Vehicle

class IsVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.verified

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.method in permissions.SAFE_METHODS)

class IsFleetOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner of a vehicle or the owner of the fleet to modify it.
    """

    def has_permission(self, request, view):
        # Check if the user is the owner of the fleet.
        # If not, deny access to the entire view.
        fleet_id = view.kwargs.get('fleet_id')  # Adjust this based on your URL configuration
        try:
            fleet = Fleet.objects.get(id=fleet_id)
            return fleet.user == request.user
        except Fleet.DoesNotExist:
            return False
    
class IsVehicleOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner of a vehicle or the owner of the fleet to modify it.
    """
    def has_permission(self, request, view):
        # Check if the user is the owner of the fleet.
        # If not, deny access to the entire view.
        vehicle_id = view.kwargs.get('vehicle_id')  # Adjust this based on your URL configuration
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            return vehicle.fleet.user == request.user
        except Vehicle.DoesNotExist:
            return False

