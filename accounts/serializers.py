# serializers.py
from rest_framework import serializers
from .models import CustomUser
from rest_framework.exceptions import MethodNotAllowed

class SignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class AdditionalInfoSerializer(serializers.ModelSerializer):
    http_method_names = ['patch']
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'first_name', 'last_name']



# signin endpoint
class SigninSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'role', 'profile_picture', 'verified']



class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CompletePasswordResetSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)