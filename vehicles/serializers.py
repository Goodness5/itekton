from rest_framework import serializers
from .models import Vehicle, Driver, Location
from fleets.models import Fleet
class DriverSerializer(serializers.ModelSerializer):
    drivers_image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True, allow_null=True, required=False)
    fleet_name = serializers.SerializerMethodField()
    vehicle = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        exclude = ['fleet']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        fleet_id = data.get('fleet')
        if fleet_id:
            try:
                fleet = Fleet.objects.get(pk=fleet_id)
                data['fleet_name'] = fleet.company_name if fleet else None
            except Fleet.DoesNotExist:
                pass
        return data

    def get_fleet_name(self, obj):
        return obj.fleet.company_name if obj.fleet else None

    def get_vehicle(self, obj):
        try:
            vehicle = Vehicle.objects.get(driver=obj)
            return {
                'id': vehicle.id,
                'identification_number': vehicle.vehicle_identification_number,
                'make': vehicle.make,
                'meter': vehicle.meter,
                'fuel_type': vehicle.fuel_type,
                'color': vehicle.color,
            }
        except Vehicle.DoesNotExist:
            return None

class DriverWithoutVehicleSerializer(serializers.ModelSerializer):
    drivers_image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True, allow_null=True, required=False)
    fleet_name = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        exclude = ['fleet']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    def get_fleet_name(self, obj):
        return obj.fleet.company_name if obj.fleet else None



# serializers.py
class VehicleSerializer(serializers.ModelSerializer):
    vehicle_image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True, allow_null=True, required=False )
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all(), required=False) 
    fleet_name = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        exclude = ['fleet']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        driver_id = data.get('driver')
        if driver_id:
            try:
                driver = Driver.objects.get(pk=driver_id, fleet=instance.fleet)
                data['driver'] = DriverWithoutVehicleSerializer(driver).data
            except Driver.DoesNotExist:
                pass
        return data

    def get_fleet_name(self, obj):
        return obj.fleet.company_name if obj.fleet else None






# class VehicleWithLocationSerializer(serializers.ModelSerializer):
#     location = LocationSerializer(many=True)
#     # vehicle = serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model = Vehicle
#         fields = ['location']
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['timestamp', 'latitude', 'longitude']

class VehicleLocationAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'assigned_location']
# Token 607e388f53a0a3eb342a8262e87098d7a346701e