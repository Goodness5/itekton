from django.db import models
from accounts.models import CustomUser 

class Fleet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    registration_id = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='company_logos/')
