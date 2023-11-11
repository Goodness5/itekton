# models.py
# from django.db import models
from fleets.models import Fleet

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models

class Vehicle(models.Model):
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')  
    vehicle_identification_number = models.CharField(max_length=50, default='')  
    make = models.CharField(max_length=50, default='')  
    meter = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    fuel_type = models.CharField(max_length=20, default='')  
    color = models.CharField(max_length=20, default='')  
    vehicle_image = models.ImageField(upload_to='vehicle_images/', null=True)
    driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, blank=True)
    # Add a field for the assigned location (boundaries of the trip)
    assigned_location = models.PointField(null=True, blank=True)

    def set_assigned_location(self, coordinates):
        # Extract latitude and longitude from the coordinates
        latitude, longitude = coordinates.split(', ')
        # Set the assigned location using a Point object
        print(latitude, longitude)
        self.assigned_location = Point(float(longitude), float(latitude))

    def get_assigned_location_coordinates(self):
        
        return list(self.assigned_location.coords[0]) if self.assigned_location else []

    def __str__(self):
        return self.name

    
   
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Location.objects.create(vehicle=self)



class Driver(models.Model):
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=100, default='')  
    license_number = models.CharField(max_length=50, default='')  
    phone_number = models.CharField(max_length=15, default='')  
    drivers_image = models.ImageField(upload_to='drivers_images/', null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Location(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return f"{self.vehicle.name} - {self.timestamp}"