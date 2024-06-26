from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class userinfo(models.Model):
    username = models.CharField(max_length=150, primary_key=True)
    email = models.EmailField()
    phone = models.IntegerField()
    password = models.CharField(max_length=200)


class contactinfo(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=500)
    item = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images/')

