from django.db import models

# Create your models here.

class Tab(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    otp = models.CharField(max_length=100)
    creation_time = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

class Event(models.Model):
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, default=1)
    date = models.DateField()
    subject = models.CharField(max_length=200)

class Purchase(models.Model):
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, default=1)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    products = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Contribution(models.Model):
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, default=1)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)