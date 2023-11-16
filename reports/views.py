
from rest_framework import generics, status
from rest_framework.response import Response
from .models import TransitReport
from .serializers import TransitReportSerializer
from itekton.permissions import IsVehicleOwner, IsVerified
from rest_framework.permissions import IsAuthenticated
from vehicles.models import Vehicle

class TransitReportView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransitReportSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        return TransitReport.objects.filter(vehicle_id=vehicle_id)

    def create(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['vehicle'] = vehicle.id  # Initialize vehicle field with the provided vehicle_id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
