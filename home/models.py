from django.db import models

# Create your models here.


class Details(models.Model):
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=60)
    email = models.EmailField(primary_key=True)
    dob = models.DateField()
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=200)


def __str__(self):
    return self.name
