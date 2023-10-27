from rest_framework import serializers
from .models import Vehicle, Driver

class VehicleSerializer(serializers.ModelSerializer):
    vehicle_image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = Vehicle
        exclude = ['fleet']

class DriverSerializer(serializers.ModelSerializer):
    drivers_image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True, allow_null=True, required=False)
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Driver
        exclude = ['fleet']


