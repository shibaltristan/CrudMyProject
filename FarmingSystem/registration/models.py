from django.conf import settings
from django.db import models


class FarmerRegistration(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registration_profile')
    farmers_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    mobile_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.farmers_id} - {self.first_name} {self.last_name}'
