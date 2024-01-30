
from rest_framework import generics, status
from rest_framework.response import Response
from .models import TransitReport, Reminder, Alert, CriticalFault, Test, Registration
from .serializers import TransitReportSerializer, ReminderSerializer, CriticalFaultSerializer, AlertSerializer, TestSerializer, RegistrationSerializer
from itekton.permissions import IsVehicleOwner, IsVerified, IsFleetOwner, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from vehicles.models import Vehicle
from fleets.models import Fleet


class TransitReportInitialView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = TransitReportSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]

    def get_queryset(self):
        fleet = Fleet.objects.get(user=self.request.user)
        return TransitReport.objects.filter(fleet=fleet)

    
    def create(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = Vehicle.objects.get(id=vehicle_id)

        # Retrieve the Fleet associated with the request.user
        fleet = Fleet.objects.get(user=request.user)

        # Initialize TransitReport instance with fleet information
        transit_report = TransitReport(vehicle=vehicle, fleet=fleet)
        transit_report.description = request.data.get('description')
        
        serializer = self.get_serializer(transit_report, data=request.data)

        if serializer.is_valid():
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
        
        # Retrieve the Fleet associated with the request.user
        fleet = Fleet.objects.get(user=request.user)

        try:
            instance = TransitReport.objects.get(vehicle_id=vehicle_id, id=report_id)
        except TransitReport.DoesNotExist:
            return Response({'error': 'Transit Report not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update the TransitReport instance with fleet information
        instance.fleet = fleet
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
    permission_classes = [IsAuthenticated, IsVerified, IsFleetOwner]

    def get_queryset(self):
        fleet_id = self.kwargs.get('fleet_id')
        return Reminder.objects.filter(fleet_id=fleet_id)

    def create(self, request, *args, **kwargs):
        fleet_id = self.kwargs.get('fleet_id')

        # Check if 'vehicle_id' is present in the request data
        if 'vehicle_id' in request.data:
            vehicle = Vehicle.objects.get(id=request.data.get('vehicle_id'))
        else:
            vehicle = None

        # Initialize Registration instance
        fleet = Fleet.objects.get(pk=fleet_id)
        if vehicle is not None:
            reminder = Registration(vehicle=vehicle, fleet=fleet)
        else:
        # If 'vehicle' is None, use the Fleet
            reminder = Reminder(fleet=fleet)

        # Initialize Reminder instance with fleet and vehicle information
        reminder = Reminder(vehicle=vehicle, fleet=fleet)
        reminder.description = request.data.get('description')
        serializer = self.get_serializer(reminder, data=request.data)

        if serializer.is_valid():
            reminder.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        fleet_id = self.kwargs.get('fleet_id')
        instance = Reminder.objects.filter(fleet_id=fleet_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

class ReminderUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsFleetOwner]
    lookup_url_kwarg = 'reminder_id'

    def get_queryset(self):
        fleet_id = self.kwargs.get('fleet_id')
        reminder_id = self.kwargs.get('reminder_id')
        
        reminders = Registration.objects.filter(fleet_id=fleet_id, pk=reminder_id)
        return reminders

    def update(self, request, *args, **kwargs):
        fleet_id = self.kwargs.get('fleet_id')
        reminder_id = self.kwargs.get('reminder_id')

        # Retrieve the Fleet associated with the request.user
        fleet = Fleet.objects.get(id=fleet_id)

        try:
            instance = Reminder.objects.get(fleet_id=fleet_id, id=reminder_id)
        except Reminder.DoesNotExist:
            return Response({'error': 'Reminder not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the Reminder instance with fleet information
        instance.fleet = fleet
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        fleet_id = self.kwargs.get('fleet_id')
        reminder_id = self.kwargs.get('reminder_id')

        try:
            instance = Reminder.objects.get(fleet_id=fleet_id, id=reminder_id)
        except Reminder.DoesNotExist:
            return Response({'error': 'Reminder not found'}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
    



class AlertInitialView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Alert.objects.filter(fleet__user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Retrieve the Fleet associated with the request.user
        try:
            fleet = Fleet.objects.get(user=request.user)
        except Fleet.DoesNotExist:
            return Response({'error': "you don't have a fleet or there is an issue with your fleet"}, status=status.HTTP_400_BAD_REQUEST)
        # Check if vehicle_id is present in kwargs
        vehicle_id = request.data.get('vehicle_id')
        if vehicle_id:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            # Initialize Alert instance with fleet and vehicle information
            alert = Alert(fleet=fleet, vehicle=vehicle)
        else:
            # Initialize Alert instance with fleet information only
            alert = Alert(fleet=fleet)

        alert.description = request.data.get('description')
        serializer = self.get_serializer(alert, data=request.data)

        if serializer.is_valid():
            alert.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

class AlertUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsOwnerOrReadOnly]
    lookup_url_kwarg = 'alert_id'

    def get_queryset(self):
        alert_id = self.kwargs.get('alert_id')
        alerts = Alert.objects.filter(pk=alert_id)
        return alerts

    def update(self, request, *args, **kwargs):
        alert_id = self.kwargs.get('alert_id')

        # Retrieve the Fleet associated with the request.user
        try:
            fleet = Fleet.objects.get(user=request.user)
        except Fleet.DoesNotExist:
            return Response({'error': "you don't have a fleet or there is an issue with your fleet"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Alert.objects.get(pk=alert_id, fleet=fleet)
        except Alert.DoesNotExist:
            return Response({'error': 'alert not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        alert_id = self.kwargs.get('alert_id')
        
        try:
            instance = Alert.objects.get(id=alert_id, fleet__user=self.request.user)
        except Alert.DoesNotExist:
            return Response({'error': 'alert not found'}, status=status.HTTP_404_NOT_FOUND)
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)






class CriticalFaultInitialView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CriticalFaultSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]

    def get_queryset(self):
        fleet = Fleet.objects.get(user=self.request.user)
        return CriticalFault.objects.filter(fleet=fleet)
    
    def create(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        try:
            fleet = Fleet.objects.get(user=request.user)
        except Fleet.DoesNotExist:
            return Response({'error': "you don't have a fleet or there is an issue with your fleet"}, status=status.HTTP_400_BAD_REQUEST)
        # Initialize CriticalFault instance
        critical_fault = CriticalFault(vehicle=vehicle, fleet=fleet)
        # Set the description from the request data
        critical_fault.description = request.data.get('description')
        serializer = self.get_serializer(critical_fault, data=request.data)

        if serializer.is_valid():
            critical_fault.save()
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
    lookup_url_kwarg = 'critical_fault_id'

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        critical_fault_id = self.kwargs.get('critical_fault_id')
        print(f'vehicle_id: {vehicle_id}, critical_fault_id: {critical_fault_id}')
        critical_faults = CriticalFault.objects.filter(vehicle_id=vehicle_id, pk=critical_fault_id)
        return critical_faults
    
    def update(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        critical_fault_id = self.kwargs.get('critical_fault_id')

        try:
            fleet = Fleet.objects.get(user=request.user)
        except Fleet.DoesNotExist:
            return Response({'error': "you don't have a fleet or there is an issue with your fleet"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = CriticalFault.objects.get(vehicle_id=vehicle_id, id=critical_fault_id, fleet=fleet)
        except CriticalFault.DoesNotExist:
            return Response({'error': 'fault not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        critical_fault_id = self.kwargs.get('critical_fault_id')
        
        try:
            instance = CriticalFault.objects.get(vehicle_id=vehicle_id, id=critical_fault_id)
        except CriticalFault.DoesNotExist:
            return Response({'error': 'fault not found'}, status=status.HTTP_404_NOT_FOUND)
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class TestInitialView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwner]

    def get_queryset(self):
        fleet = Fleet.objects.get(user=self.request.user)
        return Test.objects.filter(fleet=fleet)
    
    def create(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = Vehicle.objects.get(id=vehicle_id)

        # Get the Fleet associated with the request.user
        fleet = Fleet.objects.get(user=request.user)

        # Initialize Test instance with fleet information
        test = Test(vehicle=vehicle, fleet=fleet)
        # Set the outcome from the request data
        test.description = request.data.get('description')
        test.outcome = request.data.get('outcome')
        serializer = self.get_serializer(test, data=request.data)

        if serializer.is_valid():
            test.save()
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
    lookup_url_kwarg = 'test_id'

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        test_id = self.kwargs.get('test_id')
        print(f'vehicle_id: {vehicle_id}, test_id: {test_id}')
        tests = Test.objects.filter(vehicle_id=vehicle_id, pk=test_id)
        return tests
    
    def update(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        test_id = self.kwargs.get('test_id')
        
        try:
            instance = Test.objects.get(vehicle_id=vehicle_id, id=test_id)
        except Test.DoesNotExist:
            return Response({'error': 'test not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('vehicle_id')
        test_id = self.kwargs.get('test_id')
        
        try:
            instance = Test.objects.get(vehicle_id=vehicle_id, id=test_id)
        except Test.DoesNotExist:
            return Response({'error': 'test not found'}, status=status.HTTP_404_NOT_FOUND)
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class RegistrationInitialView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsFleetOwner]


    def get_queryset(self):
        fleet_id = self.kwargs.get('fleet_id')
        return Registration.objects.filter(fleet_id=fleet_id)
    
    def create(self, request, *args, **kwargs):
        fleet_id = self.kwargs.get('fleet_id')

        # Check if 'vehicle_id' is present in the request data
        if 'vehicle_id' in request.data:
            vehicle = Vehicle.objects.get(id=request.data.get('vehicle_id'))
        else:
            vehicle = None

        # Initialize Registration instance
        fleet = Fleet.objects.get(pk=fleet_id)
        if vehicle is not None:
            registration = Registration(vehicle=vehicle, fleet=fleet)
        else:
        # If 'vehicle' is None, use the Fleet
            registration = Registration(fleet=fleet)

        # Set the outcome from the request data
        registration.description = request.data.get('description')
        registration.expiration_date = request.data.get('expiration_date')

        serializer = self.get_serializer(registration, data=request.data)

        if serializer.is_valid():
            registration.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        fleet_id = self.kwargs.get('fleet_id')
        instance = Registration.objects.filter(vehicle__fleet_id=fleet_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

class RegistrationUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsFleetOwner]
    lookup_url_kwarg = 'registration_id'

    def get_queryset(self):
        fleet_id = self.kwargs.get('fleet_id')
        registration_id = self.kwargs.get('registration_id')
        print(f'fleet_id: {fleet_id}, registration_id: {registration_id}')
        registrations = Registration.objects.filter(fleet_id=fleet_id, pk=registration_id)
        return registrations
    
    def update(self, request, *args, **kwargs):
        fleet_id = self.kwargs.get('fleet_id')
        registration_id = self.kwargs.get('registration_id')

        try:
            instance = Registration.objects.get(fleet_id=fleet_id, id=registration_id)
        except Registration.DoesNotExist:
            return Response({'error': 'registration reminder not found'}, status=status.HTTP_404_NOT_FOUND)

        if 'vehicle_id' in request.data:
            vehicle = Vehicle.objects.get(id=request.data.get('vehicle_id'))
            # Update the instance with the new vehicle
            instance.vehicle = vehicle
        else:
            # If 'vehicle_id' is not in request.data, set 'vehicle' to None
            instance.vehicle = None

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        fleet_id = self.kwargs.get('fleet_id')
        registration_id = self.kwargs.get('registration_id')
        try:
            instance = Registration.objects.get(fleet_id=fleet_id, id=registration_id)
        except Registration.DoesNotExist:
            return Response({'error': 'registration reminder not found'}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
    
# TODO: download reports endpoints for transit reports