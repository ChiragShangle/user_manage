from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import EmailField
# Create your models here.


class Details(models.Model):
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=60)
    email = models.EmailField(primary_key=True)
    dob = models.DateField()
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, default="")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Addinfo(models.Model):
    email = models.EmailField(primary_key=True, default="")
    designation = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    is_submitted = models.BooleanField(default=False)
    city = models.CharField(max_length=60)
    pin = models.IntegerField()
    officeno = models.CharField(max_length=10)

    def __str__(self):
        return self.designation
