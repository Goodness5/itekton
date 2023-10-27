from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, AdditionalInfoSerializer, SigninSerializer
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework.authtoken.models import Token
from .serializers import CustomUserDetailSerializer
from drf_yasg.utils import swagger_auto_schema


class SignupView(generics.CreateAPIView):
    """Register  user here with email and password"""
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response({
                'message': 'User registered successfully.',
                **response.data
            }, status=status.HTTP_201_CREATED)
        else:
            return response

class AdditionalInfoView(generics.RetrieveUpdateAPIView):
    """complete user Registration takes in first name, last name and phone number and user id as a url slug"""
    http_method_names = ['patch']
    serializer_class = AdditionalInfoSerializer
    queryset = CustomUser.objects.all()
     
    def get_object(self):
        user_id = self.kwargs['pk']
        return CustomUser.objects.get(id=user_id)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)




class SigninView(generics.CreateAPIView):
    """Login a user here with email and password"""
    serializer_class = SigninSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'profile_picture': user.profile_picture.url if user.profile_picture else None,
                    # Add other user attributes as needed
                },
                'message': 'Authentication successful.'
            }, status=status.HTTP_200_OK)
        else:
            # Check specific reasons for authentication failure
            user = CustomUser.objects.filter(email=email).first()

            if user is None:
                error_message = 'User with this email does not exist.'
            elif not user.check_password(password):
                error_message = 'Incorrect password.'
            else:
                error_message = 'Authentication failed for an unknown reason.'

            return Response({
                'error': error_message,
                'message': 'Authentication failed.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(generics.RetrieveAPIView):
    """Get a user details from tthe user table by passing the user id as a slug"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserDetailSerializer


class UserListView(generics.ListAPIView):
    """Retrieves data for all users """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserDetailSerializer