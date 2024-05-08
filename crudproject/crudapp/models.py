from django.db import models
from django.utils.text import slugify



class Employee(models.Model):
    employee_name=models.CharField(max_length=255,null=True)
    department=models.CharField(max_length=255,null=True)
    age=models.IntegerField(null=True)
    email=models.EmailField(null=True)
    contact_number=models.CharField(max_length=255,null=True)