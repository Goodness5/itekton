
from rest_framework import generics, status
from rest_framework.response import Response
from .models import TransitReport, Reminder
from .serializers import TransitReportSerializer
from itekton.permissions import IsVehicleOwner, IsVerified
from rest_framework.permissions import IsAuthenticated
from vehicles.models import Vehicle

class TransitReportInitialView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = TransitReportSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        return TransitReport.objects.filter(vehicle_id=vehicle_id)
    
    def create(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        # Initialize TransitReport instance
        transit_report = TransitReport(vehicle=vehicle)
        # Set the description from the request data
        transit_report.description = request.data.get('description')
        serializer = self.get_serializer(transit_report)
        if serializer:
            transit_report.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        instance = TransitReport.objects.filter(vehicle_id=vehicle_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
class TransitReportUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransitReportSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]
    lookup_url_kwarg = 'report_id'

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        print(f'vehicle_id: {vehicle_id}, report_id: {report_id}')
        reports = TransitReport.objects.filter(vehicle_id=vehicle_id, pk=report_id)
        return reports
    
    def update(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        try:
            instance = TransitReport.objects.get(vehicle_id=vehicle_id, id=report_id)
        except TransitReport.DoesNotExist:
            return Response({'error': 'Transit Report not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        try:
            instance = TransitReport.objects.get(vehicle_id=vehicle_id, id=report_id)
        except TransitReport.DoesNotExist:
            return Response({'error': 'Transit Report not found'}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
    




class ReminderInitialView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = TransitReportSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        return Reminder.objects.filter(vehicle_id=vehicle_id)
    
    def create(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        # Initialize Reminder instance
        transit_report = Reminder(vehicle=vehicle)
        # Set the description from the request data
        transit_report.description = request.data.get('description')
        serializer = self.get_serializer(transit_report)
        if serializer:
            transit_report.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        instance = TransitReport.objects.filter(vehicle_id=vehicle_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
class ReminderUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransitReportSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]
    lookup_url_kwarg = 'report_id'

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        print(f'vehicle_id: {vehicle_id}, report_id: {report_id}')
        reports = TransitReport.objects.filter(vehicle_id=vehicle_id, pk=report_id)
        return reports
    
    def update(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        try:
            instance = TransitReport.objects.get(vehicle_id=vehicle_id, id=report_id)
        except TransitReport.DoesNotExist:
            return Response({'error': 'Transit Report not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        try:
            instance = TransitReport.objects.get(vehicle_id=vehicle_id, id=report_id)
        except TransitReport.DoesNotExist:
            return Response({'error': 'Transit Report not found'}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)