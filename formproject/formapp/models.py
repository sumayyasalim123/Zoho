from django.db import models

# Create your models here.
class employee(models.Model):
    empid = models.IntegerField(null=True)
    emp_name = models.CharField(max_length=25,null=True)
    emp_address = models.CharField(max_length=25,null=True)
    emp_email=models.EmailField(null=True)