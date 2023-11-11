from rest_framework import permissions

class IsVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.verified

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.method in permissions.SAFE_METHODS)

class IsVehicleOwnerOrFleetOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner of a vehicle or the owner of the fleet to modify it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the vehicle or the owner of the fleet.
        return obj.fleet.user == request.user 
