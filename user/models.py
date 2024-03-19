from django.db import models
from django.utils import timezone
import datetime

CITY_CHOICES = (
    ("TEHRAN", "تهران"),  # Consider adding more cities if needed
)

USER_TYPE_CHOICES = (
    ("RIDER", "Rider"),
    ("DRIVER", "Driver"),
)


class User(models.Model):
    '''
    Represents a user in the system, either a rider or driver.
    '''
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    city = models.CharField(max_length=100, choices=CITY_CHOICES)
    phone_number = models.BigIntegerField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.user_type})"

class OTP(models.Model):
    """
    Represents a one-time password (OTP) sent to a user's phone number for verification. 
    """
    phone_number = models.CharField(max_length=20)
    otp = models.CharField(max_length=5)
    expiration_time = models.DateTimeField(
        default=timezone.now() + datetime.timedelta(minutes=5), editable=False)

class Address(models.Model):
    """
    Represents a physical address associated with a user or delivery.
    """
    address = models.CharField(max_length=300)
    customer_name = models.CharField(max_length=300)
    phone_number = models.BigIntegerField()
    plaque = models.SmallIntegerField()
    unit = models.SmallIntegerField()
    description = models.TextField(blank=True)

class Deliver(models.Model):
    """
    Represents a delivery task to be completed by a driver.
    """
    origin = models.ForeignKey(Address,on_delete=models.CASCADE,related_name='deliveries_as_origin')   
    destination = models.ForeignKey(Address,on_delete=models.CASCADE, related_name='deliveries_as_destination')
    driver = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Delivery from {self.origin} to {self.destination} (driver: {self.driver})"