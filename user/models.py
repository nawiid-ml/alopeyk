from django.db import models
from django.utils import timezone
import datetime

CITY_CHOICES = (
    ("TEHRAN", "تهران"),
)

USER_TYPE_CHOICES = (
    ("RIDER", "Rider"),
    ("DRIVER", "Driver"),
)


class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    city = models.CharField(max_length=100, choices=CITY_CHOICES)
    phone_number = models.BigIntegerField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    location = models.CharField(blank=True, null=True, max_length=20)


class OTP(models.Model):
    phone_number = models.CharField(max_length=20)
    otp = models.CharField(max_length=5)
    expiration_time = models.DateTimeField(
        default=timezone.now() + datetime.timedelta(minutes=5), editable=False)

class Address(models.Model):
    address = models.CharField(max_length=300)
    customer_name = models.CharField(max_length=300)
    phone_number = models.BigIntegerField()
    plaque = models.SmallIntegerField()
    unit = models.SmallIntegerField()
    description = models.TextField(blank=True)

class Deliver(models.Model):
    origin = models.ForeignKey(Address,on_delete=models.CASCADE,related_name='deliveries_as_origin')   
    destination = models.ForeignKey(Address,on_delete=models.CASCADE, related_name='deliveries_as_destination')
    driver = models.ForeignKey(User,on_delete=models.CASCADE)