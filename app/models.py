from django.db import models

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

class Event(models.Model):
    date = models.DateField()
    subject = models.CharField(max_length=200)

class Purchase(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    products = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Contribution(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)