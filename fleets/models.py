from django.db import models
from accounts.models import CustomUser 

class Fleet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    registration_id = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='company_logos/')
    verification_otp = models.CharField(max_length=5, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)