from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Fleet
from .serializers import FleetSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class FleetListView(generics.ListCreateAPIView):
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FleetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
