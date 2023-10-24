from django.db import models
from fleets.models import Fleet

class Vehicle(models.Model):
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE)
    # Add other vehicle details here

class Driver(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)