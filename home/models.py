from django.db import models
from django.contrib.auth.models import User
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
    auth_token = models.CharField(max_length=100)
    forget_password_token = models.CharField(max_length=100, default="")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name
