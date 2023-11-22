from django.db import models
from fleets.models import Fleet
from vehicles.models import Vehicle
from django.utils import timezone

class TransitReport(models.Model):
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE, default=None)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True) 
    description = models.TextField()

    def __str__(self):
        return f'TransitReport-{self.id}'

class Reminder(models.Model):
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True, default=None)
    date = models.DateTimeField(auto_now_add=True) 
    description = models.TextField()

class Alert(models.Model):
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True, default=None)
    date = models.DateTimeField(auto_now_add=True) 
    description = models.TextField()

class CriticalFault(models.Model):
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True) 
    description = models.TextField()

class Test(models.Model):
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True) 
    description = models.TextField(default='N/A')
    outcome = models.BooleanField()  

class Registration(models.Model):
    class Status(models.TextChoices):
        OVERDUE = 'overdue', 'OverDue'
        SOON = 'soon', 'Soon'
        COMPLETED = 'completed', 'Completed'

    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True, default=None)
    expiration_date = models.DateTimeField() 
    description = models.TextField(default='N/A')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.COMPLETED,
    )

    def __str__(self):
        return f'Registration-{self.id} ({self.status})'

    def save(self, *args, **kwargs):
        current_datetime = timezone.now()

        # Ensure expiration_date is a datetime object
        if isinstance(self.expiration_date, str):
            # Adjust the format to handle milliseconds and UTC 'Z'
            try:
                self.expiration_date = timezone.datetime.strptime(self.expiration_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                # Handle cases where milliseconds are not present
                self.expiration_date = timezone.datetime.strptime(self.expiration_date, "%Y-%m-%dT%H:%M:%SZ")

        # Make current_datetime naive
        current_datetime = current_datetime.replace(tzinfo=None)

        if self.expiration_date < current_datetime:
            self.status = Registration.Status.OVERDUE
        elif current_datetime < self.expiration_date < (current_datetime + timezone.timedelta(days=30)):
            self.status = Registration.Status.SOON
        else:
            self.status = Registration.Status.COMPLETED

        super().save(*args, **kwargs)