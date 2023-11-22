from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from fleets.models import Fleet
from vehicles.models import Vehicle

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj == request.user:
            return True
        else:
            raise PermissionDenied(detail="You do not have permission to perform this action.")

class IsVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.verified:
            return True
        else:
            raise PermissionDenied(detail="You need to be a verified user to perform this action.")

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and (request.user.is_superuser or request.method in permissions.SAFE_METHODS):
            return True
        else:
            raise PermissionDenied(detail="You do not have permission to perform this action.")

class IsFleetOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner of a fleet to modify it.
    """

    def has_permission(self, request, view):
        fleet_id = view.kwargs.get('fleet_id')
        try:
            fleet = Fleet.objects.get(id=fleet_id)
            if fleet.user == request.user:
                return True
            else:
                raise PermissionDenied(detail="You do not have permission to perform this action.")
        except Fleet.DoesNotExist:
            raise PermissionDenied(detail="Fleet does not exist.")
        
        

class IsVehicleOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner of a vehicle or the owner of the fleet to modify it.
    """
    def has_permission(self, request, view):
        vehicle_id = view.kwargs.get('vehicle_id')
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            if vehicle.fleet.user == request.user:
                return True
            else:
                raise PermissionDenied(detail="You do not have permission to perform this action.")
        except Vehicle.DoesNotExist:
            raise PermissionDenied(detail="Vehicle does not exist.")
