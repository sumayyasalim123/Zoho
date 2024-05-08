from django.db import models

# Create your models here.

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    user_name=models.CharField(max_length=255)
    email=models.EmailField()
    password = models.CharField(max_length=255)  
    cpassword = models.CharField(max_length=255, null=True, blank=True, default=None)

    