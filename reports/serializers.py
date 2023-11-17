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
    class Meta:
        model = Reminder
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'

class CriticalFaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriticalFault
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
