from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Vehicle, Driver, Location
from .serializers import VehicleSerializer, DriverSerializer, LocationSerializer, VehicleLocationAssignmentSerializer
from itekton.permissions import IsVerified, IsVehicleOwnerOrFleetOwner
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
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
        
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        # Add fleet and vehicle names to each record
        for item in data:
            vehicle_id = item.get('id')
            try:
                vehicle = Vehicle.objects.get(pk=vehicle_id, fleet=self.request.user.fleet)
                item['fleet_name'] = vehicle.fleet.company_name if vehicle.fleet else None
                item['vehicle_name'] = vehicle.name or '' 
            except Vehicle.DoesNotExist:
                item['fleet_name'] = None
                item['vehicle_name'] = None

        return Response(data)

class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated, IsVerified]
    


    def perform_update(self, serializer):
        driver_id = self.request.data.get('driver_id')
        if driver_id:
            try:
                driver = Driver.objects.get(pk=driver_id, fleet=self.request.user.fleet)
                serializer.save(driver=driver)
            except Driver.DoesNotExist:
                return Response({'error': 'Invalid driver ID or unauthorized'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
    



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
                    # Check if the vehicle is already assigned to a driver
                    if vehicle.driver is None:
                        serializer.save(vehicle_id=vehicle_id, fleet=self.request.user.fleet)
                    else:
                        return Response({'error': 'Vehicle already assigned to a driver'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer.save(fleet=self.request.user.fleet)
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
                # Check if the vehicle is already assigned to a driver
                if vehicle.driver is None:
                    serializer.save(vehicle_id=vehicle_id, fleet=self.request.user.fleet)
                else:
                    return Response({'error': 'Vehicle already assigned to a driver'}, status=status.HTTP_400_BAD_REQUEST)
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


@api_view(['POST'])  
@permission_classes([IsAuthenticated, IsVerified])  
def unassign_driver_from_vehicle(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(pk=vehicle_id, fleet=request.user.fleet)
        vehicle.driver = None
        vehicle.save()
        return Response({'message': 'Driver unassigned successfully'}, status=status.HTTP_200_OK)
    except Vehicle.DoesNotExist:
        return Response({'error': 'Vehicle does not exist or unauthorized'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])  
@permission_classes([IsAuthenticated, IsVerified])      
def assign_driver_to_vehicle(request, vehicle_id, driver_id):
    try:
        vehicle = Vehicle.objects.get(pk=vehicle_id, fleet=request.user.fleet)
        driver = Driver.objects.get(pk=driver_id, fleet=request.user.fleet)
        
        # Check if the vehicle is already assigned to a driver
        if vehicle.driver:
            return Response({'error': 'vehicle is already asigned to a driver'}, status=status.HTTP_400_BAD_REQUEST)
        
        vehicle.driver = driver
        vehicle.save()
        return Response({'message': 'Driver assigned successfully'}, status=status.HTTP_200_OK)
    
    except Vehicle.DoesNotExist:
        return Response({'error': 'Vehicle does not exist or unauthorized'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Driver.DoesNotExist:
        return Response({'error': 'Driver does not exist or unauthorized'}, status=status.HTTP_400_BAD_REQUEST)
    

class LocationListView(generics.CreateAPIView):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsVerified]

    def get_queryset(self):
        vehicle_id = self.kwargs['pk']
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            locations = Location.objects.filter(vehicle=vehicle)
            return locations
        except Vehicle.DoesNotExist:
            return Location.objects.none()

    def create(self, request, *args, **kwargs):
        vehicle_id = self.kwargs['pk']
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            location = Location.objects.create(vehicle=vehicle, latitude=latitude, longitude=longitude)
            serializer = self.get_serializer(location)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsVerified]


    # def get_queryset(self):
    #     vehicle_id = self.kwargs['pk']
    #     try:
    #         vehicle = Vehicle.objects.get(id=vehicle_id)
    #         locations = Location.objects.filter(vehicle=vehicle)
    #         return locations
    #     except Vehicle.DoesNotExist:
    #         return Location.objects.none()


    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, many=True)
    #     return Response(serializer.data)


class VehicleLocationAssignmentView(generics.CreateAPIView, generics.RetrieveUpdateAPIView):
    serializer_class = VehicleLocationAssignmentSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsVehicleOwnerOrFleetOwner]
    queryset = Vehicle.objects.all()

    def get(self, request, *args, **kwargs):
        # Access the vehicle ID from kwargs
        vehicle_id = kwargs.get('vehicle_id')

        try:
            # Retrieve the vehicle model
            vehicle = Vehicle.objects.get(id=vehicle_id)

            # Retrieve the location associated with the vehicle
            # location = Location.objects.get(vehicle=vehicle)

            # Serialize the data
            assigned_location_serilizer = VehicleLocationAssignmentSerializer(vehicle)
            vehicle_serializer = VehicleSerializer(vehicle)

            # Return a combined response
            return Response({
                'assigned_location': assigned_location_serilizer.data
            }, status=status.HTTP_200_OK)

        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, vehicle_id):
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            serializer = VehicleLocationAssignmentSerializer(data=request.data)

            if serializer.is_valid():
                # Extract coordinates from the request data
                coordinates = serializer.validated_data.get('assigned_location')

                # Set the assigned location for the vehicle
                vehicle.set_assigned_location(coordinates)

                # Ensure the fleet is set before saving
                if vehicle.fleet is None:
                    return Response({'error': 'Fleet information is required'}, status=status.HTTP_400_BAD_REQUEST)

                vehicle.save()
                return Response('saved successfull', status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
