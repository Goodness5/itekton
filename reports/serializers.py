from rest_framework import serializers
from .models import TransitReport, Reminder, Alert, CriticalFault, Test, Registration
from vehicles.serializers import VehicleSerializer
from vehicles.models import Vehicle

class TransitReportSerializer(serializers.ModelSerializer):
    vehicle = serializers.SerializerMethodField()
    # vehicle_id = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = TransitReport
        fields = ['id', 'vehicle', 'date', 'description']
        read_only_fields = ['date']

    def get_vehicle(self, obj):
        try:
            vehicle = Vehicle.objects.get(pk=obj.vehicle.id)
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
        



class ReminderSerializer(serializers.ModelSerializer):
    vehicle = serializers.SerializerMethodField()
    vehicle_id = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = Reminder
        fields = ['id', 'vehicle_id', 'vehicle', 'date', 'description']
        read_only_fields = ['date']

    def get_vehicle(self, obj):
        try:
            vehicle = Vehicle.objects.get(pk=obj.vehicle_id)
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

class AlertSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.IntegerField(write_only=True, required=False)
    vehicle = serializers.SerializerMethodField()
    
    class Meta:
        model = Alert
        fields = ['id', 'vehicle_id', 'vehicle', 'date', 'description']
        read_only_fields = ['date']

    def validate(self, data):
        vehicle_id = data.get('vehicle_id')
        if vehicle_id:
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id)
            except Vehicle.DoesNotExist:
                raise serializers.ValidationError("Invalid vehicle_id.")
            data['vehicle'] = vehicle
        return data
    
    def get_vehicle(self, obj):
        try:
            vehicle = Vehicle.objects.get(pk=obj.vehicle_id)
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


class CriticalFaultSerializer(serializers.ModelSerializer):
    vehicle = serializers.SerializerMethodField()
    # vehicle_id = serializers.IntegerField(write_only=True, required=False)
    

    def get_vehicle(self, obj):
        try:
            vehicle = Vehicle.objects.get(pk=obj.vehicle.id)
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
    class Meta:
        model = CriticalFault
        fields = ['id', 'vehicle', 'date', 'description']
        read_only_fields = ['date']

class TestSerializer(serializers.ModelSerializer):
    vehicle = serializers.SerializerMethodField()
    class Meta:
        model = Test
        fields = ['id', 'description', 'vehicle', 'date', 'outcome']
        read_only_fields = ['date']

    def get_vehicle(self, obj):
        try:
            vehicle = Vehicle.objects.get(pk=obj.vehicle_id)
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
class RegistrationSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), required=False, write_only=True)
    vehicle = serializers.SerializerMethodField()
    class Meta:
        model = Registration
        fields = ['id', 'vehicle', 'vehicle_id', 'expiration_date', 'description']
        read_only_fields = ['date', 'vehicle']

    def create(self, validated_data):
        # Extract 'vehicle_id' from validated_data
        vehicle_id = validated_data.pop('vehicle_id', None)

        # If 'vehicle_id' is provided, get the corresponding Vehicle
        vehicle = None
        if vehicle_id is not None:
            vehicle = Vehicle.objects.get(id=vehicle_id)

        # Create the Registration instance
        registration = Registration(vehicle=vehicle, **validated_data)
        registration.save()

        return registration
    
    def get_vehicle(self, obj):
        try:
            vehicle = Vehicle.objects.get(pk=obj.vehicle_id)
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