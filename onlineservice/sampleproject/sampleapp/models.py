from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
     user_type = models.CharField(default=1, max_length=10,null=True)

class Usermember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    c_number = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    profilepic = models.ImageField(blank=True, upload_to="image/", null=True)
    confirmation_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name}'s Profile"

class Categories(models.Model):
    category_name = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=10, default='1', null=True)

    def __str__(self):
        return self.category_name

class UserMember1(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True, related_name='usermember1_categories')
    a_ddress = models.CharField(max_length=255,null=True)
    contactnumber = models.CharField(max_length=255,null=True)
    experience = models.CharField(default=1, max_length=25,null=True)
    dob = models.DateField(null=True, blank=True)

    new_dept = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True, related_name='usermember1_new_dept')
    id_type = models.CharField(max_length=255,null=True)
    profile_picture = models.ImageField(upload_to="images/", null=True, blank=True)
    certificate = models.FileField(upload_to="certificates/", null=True, blank=True)
    status = models.CharField(max_length=10, default='1', null=True)

    

    
  
