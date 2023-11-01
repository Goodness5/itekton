# models.py
from django.db import models
from fleets.models import Fleet

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

    def __str__(self):
        return self.name

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
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.vehicle.name} - {self.timestamp}"

