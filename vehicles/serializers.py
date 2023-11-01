from rest_framework import serializers
from .models import Vehicle, Driver, Location
class DriverSerializer(serializers.ModelSerializer):
    drivers_image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True, allow_null=True, required=False)
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), required=False) 
    
    class Meta:
        model = Driver
        exclude = ['fleet']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        vehicle_id = data.get('vehicle')
        if vehicle_id:
            try:
                vehicle = Vehicle.objects.get(pk=vehicle_id, fleet=instance.fleet)
                data['vehicle'] = VehicleSerializer(vehicle).data
            except Vehicle.DoesNotExist:
                pass
        return data

class VehicleSerializer(serializers.ModelSerializer):
    vehicle_image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True)
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all(), required=False) 

    class Meta:
        model = Vehicle
        exclude = ['fleet']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        driver_id = data.get('driver')
        if driver_id:
            try:
                driver = Driver.objects.get(pk=driver_id, fleet=instance.fleet)
                data['driver'] = DriverSerializer(driver).data
            except Driver.DoesNotExist:
                pass
        return data


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'timestamp']

# Token 607e388f53a0a3eb342a8262e87098d7a346701e