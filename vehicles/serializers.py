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
        vehicles = Vehicle.objects.filter(driver=obj)
        if vehicles.exists():
            return [
                {
                    'id': vehicle.id,
                    'identification_number': vehicle.vehicle_identification_number,
                    'make': vehicle.make,
                    'meter': vehicle.meter,
                    'fuel_type': vehicle.fuel_type,
                    'color': vehicle.color,
                }
            for vehicle in vehicles
            ]
        else:
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


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_image = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all(), required=False)
    name = serializers.CharField(required=True)
    meter = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    make = serializers.CharField(required=True)
    fuel_type = serializers.CharField(required=True)
    color = serializers.CharField(required=True)
# Token c39a46c0f4f7a9d5cd2fbffbf09dab25eaabafae
    # Add 'name' and 'meter' fields and set them as required

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

    # def get_fleet_name(self, obj):
    #     return obj.fleet.company_name if obj.fleet else None






# class VehicleWithLocationSerializer(serializers.ModelSerializer):
#     location = LocationSerializer(many=True)
#     # vehicle = serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model = Vehicle
#         fields = ['location']
class LocationSerializer(serializers.ModelSerializer):
    vehicle = serializers.SerializerMethodField()

    def get_vehicle(self, obj):
        vehicle = obj.vehicle
        driver_info = {}

        if vehicle:
            driver = vehicle.driver
            if driver:
                driver_info = {
                    'driver_id': driver.id,
                    'driver_name': driver.name,
                    'driver_image': driver.drivers_image,
                    'driver_contact': driver.phone_number,
                }

        return {
            'id': vehicle.id if vehicle else None,
            'name': vehicle.name if vehicle else None,
            'fleet': {
                'id': vehicle.fleet.id if vehicle else None,
                'company_name': vehicle.fleet.company_name if vehicle else None,
                'driver': driver_info,
            },
            'timestamp': obj.timestamp,
            'latitude': obj.latitude,
            'longitude': obj.longitude,
        }

    class Meta:
        model = Location
        fields = ['timestamp', 'latitude', 'longitude', 'vehicle']



class VehicleLocationAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'assigned_location']
# Token 607e388f53a0a3eb342a8262e87098d7a346701e