import random
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Fleet
from .serializers import FleetSerializer, VerifyOTPSerializer, SendOTPSerializer, FleetWithUserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.utils import timezone
from itekton.permissions import IsVerified, IsFleetOwner, IsOwnerOrReadOnly
from accounts.models import CustomUser

class FleetListView(generics.ListCreateAPIView):
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'fleet_id'

    def create(self, request, *args, **kwargs):
        try:
            user = request.user

            # Check if the user already has a fleet
            fleet_instance = Fleet.objects.filter(user=user).first()
            if fleet_instance:
                # If a Fleet instance already exists for the user, return an error message
                return Response({'error': 'User already has a fleet', 'fleet_id': fleet_instance.id}, status=status.HTTP_400_BAD_REQUEST)

            # If no Fleet instance exists, create a new one
            serializer = FleetSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FleetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsVerified, IsFleetOwner]
    parser_classes = (MultiPartParser, FormParser)
    lookup_url_kwarg = 'fleet_id'

    def perform_update(self, serializer):
        company_name = self.request.data.get('company_name')
        registration_id = self.request.data.get('registration_id')
        address = self.request.data.get('address')
        company_logo = self.request.data.get('company_logo')
        profile_picture = self.request.data.get('profile_picture')

        fleet = serializer.save()

        if company_logo:
            fleet.company_logo = company_logo

        fleet.save()

        # Assuming you have a OneToOneField between Fleet and User
        user = fleet.user

        if company_name:
            fleet.company_name = company_name

        if registration_id:
            fleet.registration_id = registration_id

        if address:
            fleet.address = address

        fleet.save()

        if profile_picture:
            user.profile_picture = profile_picture
            user.save()

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_fleet(request):
    queryset = Fleet.objects.all()
    try:
        user = request.user 
        print(user)
        fleet_instance = Fleet.objects.get(user=user)

        if not fleet_instance:
            return Response({'error': 'User does not have a fleet'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FleetWithUserSerializer(fleet_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)





def generate_otp():
    return str(random.randint(10000, 99999))

def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP for account verification is: {otp}'
    from_email = 'goodnesskolapo@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)



class SendOTPView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SendOTPSerializer 

    def create(self, request, *args, **kwargs):
        user = request.user
        email = request.data.get('email')

        isuser = CustomUser.objects.filter(email=email)
        try:
            # Check if the provided email matches the authenticated user's email
            if not isuser:
                return Response({'error': 'user email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if email != user.email:
                return Response({'error': 'invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user is already verified
            if user.verified:
                return Response({'error': 'User is already verified.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user has a fleet
            if not hasattr(user, 'fleet'):
                return Response({'error': 'User does not have a fleet.'}, status=status.HTTP_400_BAD_REQUEST)

            fleet = user.fleet

            # Check if OTP has already been sent
            if fleet.verification_otp:
                return Response({'error': 'OTP has already been sent. Please check your email.'}, status=status.HTTP_400_BAD_REQUEST)

            otp = generate_otp()
            fleet.verification_otp = otp
            fleet.otp_created_at = timezone.now()  # Add timestamp
            fleet.save()

            # Send OTP via email
            send_otp_email(email, otp)

            return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOTPView(generics.CreateAPIView):
    serializer_class = VerifyOTPSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        otp = request.data.get('otp')

        # Check if user is already verified
        if user.verified:
            return Response({'error': 'User is already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        stored_otp = user.fleet.verification_otp
        otp_created_at = user.fleet.otp_created_at

        # Check if OTP exists and hasn't expired (e.g., 5 minutes)
        if stored_otp and otp_created_at:
            current_time = timezone.now()  # Use timezone-aware datetime
            expiration_time = otp_created_at + timedelta(minutes=5)  # Adjust duration as needed

            if current_time <= expiration_time and otp == stored_otp:
                user.verified = True
                user.save()

                # Delete the OTP
                user.fleet.verification_otp = None
                user.fleet.otp_created_at = None
                user.fleet.save()

                return Response({'message': 'Account verified successfully.'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid OTP or OTP has expired. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)