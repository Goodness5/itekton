from rest_framework import serializers
from .models import Fleet
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions


class FleetSerializer(serializers.ModelSerializer):
    company_logo = serializers.ImageField(max_length=None, use_url=True, required=False)
    profile_picture = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Fleet
        fields = ['id', 'company_name', 'registration_id', 'address', 'company_logo', 'profile_picture']

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(min_length=5, max_length=5)