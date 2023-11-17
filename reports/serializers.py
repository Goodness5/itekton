from rest_framework import serializers
from .models import TransitReport, Reminder, Alert, CriticalFault, Test, Registration
from vehicles.serializers import VehicleSerializer
from vehicles.models import Vehicle

class TransitReportSerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = TransitReport
        fields = ['id', 'vehicle', 'date', 'description']
        read_only_fields = ['date']
class ReminderSerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Reminder
        fields = ['id', 'vehicle', 'date', 'description']
        read_only_fields = ['date']

class AlertSerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Alert
        fields = ['id', 'vehicle', 'date', 'description']
        read_only_fields = ['date']

class CriticalFaultSerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = CriticalFault
        fields = ['id', 'vehicle', 'date', 'description']
        read_only_fields = ['date']

class TestSerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Test
        fields = ['id', 'vehicle', 'date', 'outcome']
        read_only_fields = ['date']
class RegistrationSerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Registration
        fields = ['id', 'vehicle', 'date', 'description']
        read_only_fields = ['date']
