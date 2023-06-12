from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

class Stock(models.Model):
    email = models.CharField(max_length=200) # storing the email should make it easier
    stock_ticker = models.CharField(max_length=10) # this shouldn't be that long
