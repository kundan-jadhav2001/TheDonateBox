from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class userinfo(models.Model):
    username = models.CharField(max_length=150, primary_key=True)
    email = models.EmailField()
    phone = models.IntegerField()
    password = models.CharField(max_length=200)


class contact(models.Model):
    name = models.ForeignKey(userinfo, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=500)
    item = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images')

