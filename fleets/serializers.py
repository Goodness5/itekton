from rest_framework import serializers
from .models import Fleet
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions


from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Fleet

class FleetSerializer(serializers.ModelSerializer):
    company_logo = serializers.ImageField(max_length=None, use_url=True, required=False)
    profile_picture = serializers.ImageField(max_length=None, use_url=True, required=False)
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Fleet
        fields = ['id', 'company_name', 'registration_id', 'address', 'company_logo', 'profile_picture', 'owner']
    
    def get_owner(self, obj):
        user = obj.user
        return {
            'id': user.id,
            'username': {user.firstname, user.lastname},
            'email': {user.email},
            'profile_picture': {user.profile_picture},
        }
    def create(self, validated_data):
        # Handle company-related fields
        company_name = validated_data.get('company_name')
        registration_id = validated_data.get('registration_id')
        address = validated_data.get('address')

        # Handle company_logo
        company_logo = validated_data.get('company_logo')

        # Handle profile_picture
        profile_picture = validated_data.get('profile_picture')

        # Get the authenticated user
        user = self.context['request'].user

        # Create Fleet instance
        fleet = Fleet.objects.create(
            company_name=company_name,
            registration_id=registration_id,
            address=address,
            company_logo=company_logo,
            user=user  # Associate the fleet with the authenticated user
        )

        # Save profile_picture in the associated User model
        if profile_picture:
            user.profile_picture = profile_picture
            user.save()

        return fleet
    


class FleetWithUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.user
        return {
            'id': user.id,
            'username': {user.firstname, user.lastname},
            'email': {user.email},
            'profile_picture': {user.profile_picture},
        }

    class Meta:
        model = Fleet
        fields = ['id', 'company_name', 'registration_id', 'address', 'company_logo', 'profile_picture', 'user']

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(min_length=5, max_length=5)