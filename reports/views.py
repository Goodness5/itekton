
from rest_framework import generics, status
from rest_framework.response import Response
from .models import TransitReport, Reminder, Alert, CriticalFault, Test
from .serializers import TransitReportSerializer, ReminderSerializer, CriticalFaultSerializer, AlertSerializer, TestSerializer
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
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        return Reminder.objects.filter(vehicle_id=vehicle_id)
    
    def create(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        # Initialize Reminder instance
        reminder = Reminder(vehicle=vehicle)
        # Set the description from the request data
        reminder.description = request.data.get('description')
        serializer = self.get_serializer(reminder)
        if serializer:
            reminder.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        instance = Reminder.objects.filter(vehicle_id=vehicle_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
class ReminderUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]
    lookup_url_kwarg = 'report_id'

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        print(f'vehicle_id: {vehicle_id}, report_id: {report_id}')
        reminders = Reminder.objects.filter(vehicle_id=vehicle_id, pk=report_id)
        return reminders
    
    def update(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        try:
            instance = Reminder.objects.get(vehicle_id=vehicle_id, id=report_id)
        except Reminder.DoesNotExist:
            return Response({'error': 'reminder not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        try:
            instance = Reminder.objects.get(vehicle_id=vehicle_id, id=report_id)
        except Reminder.DoesNotExist:
            return Response({'error': 'Reminder not found'}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
    





class AlertInitialView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        return Alert.objects.filter(vehicle_id=vehicle_id)
    
    def create(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        # Initialize Reminder instance
        alert = Alert(vehicle=vehicle)
        # Set the description from the request data
        alert.description = request.data.get('description')
        serializer = self.get_serializer(alert)
        if serializer:
            alert.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        instance = Alert.objects.filter(vehicle_id=vehicle_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
class AlertUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]
    lookup_url_kwarg = 'report_id'

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        print(f'vehicle_id: {vehicle_id}, report_id: {report_id}')
        alerts = Alert.objects.filter(vehicle_id=vehicle_id, pk=report_id)
        return alerts
    
    def update(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        try:
            instance = Alert.objects.get(vehicle_id=vehicle_id, id=report_id)
        except Alert.DoesNotExist:
            return Response({'error': 'alert not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        try:
            instance = Alert.objects.get(vehicle_id=vehicle_id, id=report_id)
        except Alert.DoesNotExist:
            return Response({'error': 'alert not found'}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
   






class CriticalFaultInitialView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CriticalFaultSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        return CriticalFault.objects.filter(vehicle_id=vehicle_id)
    
    def create(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        # Initialize Reminder instance
        criticalfaults = CriticalFault(vehicle=vehicle)
        # Set the description from the request data
        criticalfaults.description = request.data.get('description')
        serializer = self.get_serializer(criticalfaults)
        if serializer:
            criticalfaults.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        instance = CriticalFault.objects.filter(vehicle_id=vehicle_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
class CriticalFaultUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CriticalFaultSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]
    lookup_url_kwarg = 'report_id'

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        print(f'vehicle_id: {vehicle_id}, report_id: {report_id}')
        criticalaults = CriticalFault.objects.filter(vehicle_id=vehicle_id, pk=report_id)
        return criticalaults
    
    def update(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        try:
            instance = CriticalFault.objects.get(vehicle_id=vehicle_id, id=report_id)
        except CriticalFault.DoesNotExist:
            return Response({'error': 'fault not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        try:
            instance = CriticalFault.objects.get(vehicle_id=vehicle_id, id=report_id)
        except CriticalFault.DoesNotExist:
            return Response({'error': 'alert not found'}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
    



class TestInitialView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        return Test.objects.filter(vehicle_id=vehicle_id)
    
    def create(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        # Initialize Reminder instance
        tests = Test(vehicle=vehicle)
        # Set the description from the request data
        tests.description = request.data.get('outcome')
        serializer = self.get_serializer(tests)
        if serializer:
            tests.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        instance = Test.objects.filter(vehicle_id=vehicle_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
class TestUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]
    lookup_url_kwarg = 'report_id'

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        print(f'vehicle_id: {vehicle_id}, report_id: {report_id}')
        tests = Test.objects.filter(vehicle_id=vehicle_id, pk=report_id)
        return tests
    
    def update(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        try:
            instance = Test.objects.get(vehicle_id=vehicle_id, id=report_id)
        except Test.DoesNotExist:
            return Response({'error': 'test not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        report_id = self.kwargs.get('report_id')
        try:
            instance = Test.objects.get(vehicle_id=vehicle_id, id=report_id)
        except Test.DoesNotExist:
            return Response({'error': 'test not found'}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
    


# class TestInitialView(generics.ListCreateAPIView, generics.DestroyAPIView):
#     serializer_class = TestSerializer
#     permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]

#     def get_queryset(self):
#         vehicle_id = self.kwargs.get('vehicle_id')
#         return Test.objects.filter(vehicle_id=vehicle_id)
    
#     def create(self, request, *args, **kwargs):
#         vehicle_id = self.kwargs.get('vehicle_id')
#         vehicle = Vehicle.objects.get(id=vehicle_id)
#         # Initialize Reminder instance
#         tests = Test(vehicle=vehicle)
#         # Set the outcome from the request data
#         tests.description = request.data.get('description')
#         serializer = self.get_serializer(tests)
#         if serializer:
#             tests.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, *args, **kwargs):
#         vehicle_id = self.kwargs.get('vehicle_id')
#         instance = Test.objects.filter(vehicle_id=vehicle_id)
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_200_OK)
# class TestUpdateView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = TestSerializer
#     permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]
#     lookup_url_kwarg = 'report_id'

#     def get_queryset(self):
#         vehicle_id = self.kwargs.get('vehicle_id')
#         report_id = self.kwargs.get('report_id')
#         print(f'vehicle_id: {vehicle_id}, report_id: {report_id}')
#         tests = Test.objects.filter(vehicle_id=vehicle_id, pk=report_id)
#         return tests
    
#     def update(self, request, *args, **kwargs):
#         vehicle_id = self.kwargs.get('vehicle_id')
#         report_id = self.kwargs.get('report_id')
#         try:
#             instance = Test.objects.get(vehicle_id=vehicle_id, id=report_id)
#         except Test.DoesNotExist:
#             return Response({'error': 'test not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = self.get_serializer(instance, data=request.data)
#         if serializer.is_valid():
#             self.perform_update(serializer)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, *args, **kwargs):
#         vehicle_id = self.kwargs.get('vehicle_id')
#         report_id = self.kwargs.get('report_id')
#         try:
#             instance = Test.objects.get(vehicle_id=vehicle_id, id=report_id)
#         except Test.DoesNotExist:
#             return Response({'error': 'test not found'}, status=status.HTTP_404_NOT_FOUND)
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_200_OK)
    