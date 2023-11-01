
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Vehicle, Driver
from .serializers import VehicleSerializer, DriverSerializer
from itekton.permissions import IsVerified
from rest_framework.parsers import MultiPartParser, FormParser

class VehicleListView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsVerified]                

    def perform_create(self, serializer):
        try:
            serializer.save(fleet=self.request.user.fleet)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated, IsVerified]
    

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        return Response({'error': str(exc)}, status=response.status_code)
class DriverListView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated, IsVerified]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        try:
            vehicle_id = self.request.data.get('vehicle')
            if vehicle_id:
                vehicle = Vehicle.objects.get(pk=vehicle_id)
                if vehicle.fleet == self.request.user.fleet:
                    serializer.save(vehicle_id=vehicle_id, fleet=self.request.user.fleet)
                else:
                    return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer.save(fleet=self.request.user.fleet)  # Assign fleet based on user
        except Vehicle.DoesNotExist as e:
            return Response({'error': 'Vehicle does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated, IsVerified]

    def perform_update(self, serializer):
        vehicle_id = self.request.data.get('vehicle')
        if vehicle_id:
            try:
                vehicle = Vehicle.objects.get(pk=vehicle_id, fleet=self.request.user.fleet)
                serializer.save(vehicle_id=vehicle_id, fleet=self.request.user.fleet)
            except Vehicle.DoesNotExist:
                return Response({'error': 'Vehicle does not exist or unauthorized'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        return Response({'error': str(exc)}, status=response.status_code)


class FleetDriversListView(generics.ListAPIView):
    """"get all fleet drivers by passing the fleet id"""
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated, IsVerified]

    def get_queryset(self):
        fleet_id = self.kwargs['fleet_id']
        return Driver.objects.filter(vehicle__fleet_id=fleet_id)

class FleetVehiclesListView(generics.ListAPIView):
    """"get a list of all vehicles belonging to a fleet"""
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated, IsVerified]

    def get_queryset(self):
        fleet_id = self.kwargs['fleet_id']
        return Vehicle.objects.filter(fleet_id=fleet_id)
    

class FleetDriversVehiclesListView(generics.ListAPIView):
    """get all FleetDrivers and the vehicles for a fleet"""
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated, IsVerified]

    def get_queryset(self):
        fleet_id = self.kwargs['fleet_id']
        return Driver.objects.filter(vehicle__fleet_id=fleet_id)

