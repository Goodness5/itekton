from rest_framework import serializers
from .models import Fleet

class FleetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = ['company_name', 'registration_id', 'address', 'company_logo']