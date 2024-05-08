from django.db import models

# Create your models here.
class studentRegister(models.Model):
    name=models.CharField(max_length=255,null=True)
    address=models.TextField()
    age=models.IntegerField(null=True)
    email=models.EmailField()
    joiningDate=models.DateField()
    qualification=models.CharField(max_length=255)
    gender=models.CharField(max_length=255)
    mobile=models.CharField(max_length=25)