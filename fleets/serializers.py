from rest_framework import serializers
from .models import Fleet
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib.auth import get_user_model

class FleetSerializer(serializers.ModelSerializer):
    company_logo = serializers.ImageField(max_length=None, use_url=True, required=False)
    profile_picture = serializers.ImageField(source='user.profile_picture', max_length=None, use_url=True, required=False, write_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Fleet
        fields = ['id', 'company_name', 'registration_id', 'address', 'company_logo', 'profile_picture', 'user']

    def get_user(self, obj):
        user = obj.user
        profile_picture = user.profile_picture if user.profile_picture else None

        # Check if the profile picture file exists
        try:
            if profile_picture:
                with open(profile_picture.path, 'rb'):
                    pass  # File exists, do nothing
        except FileNotFoundError:
            # Log the error or handle it as needed
            print(f"Profile picture not found for user {user.id}. Using default.")
            profile_picture = None

        return {
            'id': user.id,
            'name': {user.first_name, user.last_name},
            'email': {user.email},
            'profile_picture': profile_picture,
        }
    def create(self, validated_data):
        # Handle company-related fields
        company_logo = validated_data.pop('company_logo', None)
        profile_picture = validated_data.pop('profile_picture', None)

        # Get the authenticated user
        user = self.context['request'].user

        # Create Fleet instance
        fleet = Fleet.objects.create(user=user, **validated_data)

        # Save company_logo in the Fleet model
        if company_logo:
            fleet.company_logo = company_logo
            fleet.save()

        # Save profile_picture in the associated User model
        if profile_picture:
            user.profile_picture = profile_picture
            user.save()

        return fleet


class FleetWithUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.user
        profile_picture = user.profile_picture if user.profile_picture else None

        # Check if the profile picture file exists
        try:
            if profile_picture:
                with open(profile_picture.path, 'rb'):
                    pass  # File exists, do nothing
        except FileNotFoundError:
            # Log the error or handle it as needed
            print(f"Profile picture not found for user {user.id}. Using default.")
            profile_picture = None

        return {
            'id': user.id,
            'name': {user.first_name, user.last_name},
            'email': {user.email},
            'profile_picture': profile_picture,
        }
    class Meta:
        model = Fleet
        fields = ['id', 'company_name', 'registration_id', 'address', 'company_logo', 'user']

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(min_length=5, max_length=5)