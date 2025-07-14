from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    dob = models.DateField(blank=False)
    phone = PhoneNumberField(blank=False)

class Facility(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
   

class Campsite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length= 75, null=False)
    description = models.CharField(max_length= 300, null=False)
    picture = models.URLField(null=True, blank=True)
    address1 = models.CharField(max_length= 75, null=False)
    address2 = models.CharField(max_length= 75)
    town = models.CharField(max_length= 75, null=False)
    county = models.CharField(max_length= 75)
    postcode = models.CharField(max_length= 75, null=False)
    latitude = models.FloatField()
    longitude = models.FloatField() 
    email = models.EmailField(blank=False, null=False)
    phone = PhoneNumberField(blank=False, null=False)
    facilities = models.ManyToManyField(Facility,blank=True, related_name="facilities")

class Plot(models.Model):
    class Types(models.TextChoices):
        Tent = 'Tent', ('Tent')
        Campervan = 'Campervan', ('Campervan')
        Caravan = 'Caravan', ('Caravan')
        Motorhome = 'Motorhome', ('Motorhome')
        Glamping = 'Glamping', ('Glamping')
    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE, related_name="plots")    
    name = models.CharField(max_length= 75)
    type = models.CharField(choices=Types.choices, default='Tent', max_length=10, blank=False)   
    power = models.BooleanField(blank=False)
    capacity = models.PositiveBigIntegerField(default=1, blank=False)
    length = models.PositiveBigIntegerField(default=1, blank=False)
    width = models.PositiveBigIntegerField(default=1, blank=False)
    price = models.PositiveIntegerField(default=1, blank=False)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name="booked_plot")
    arrival = models.DateField(blank=False)
    checkout = models.DateField(blank=False)
    notes = models.CharField(max_length = 300)
    people = models.PositiveIntegerField(default=1, blank=False)
    cost = models.PositiveIntegerField(default=1, blank=False)