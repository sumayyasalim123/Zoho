from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Catogories(models.Model):
    catogory_name=models.CharField(max_length=255,null=True)

class Product(models.Model):
    catogories=models.ForeignKey(Catogories,on_delete=models.CASCADE,null=True)
    add_product=models.CharField(max_length=255,null=True)
    description=models.CharField(max_length=255)
    price=models.IntegerField(null=True)
    image=models.ImageField(blank=True,upload_to="image/",null=True)


class Usermember(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
   address=models.CharField(max_length=255)
   c_number=models.CharField(max_length=255)
   profilepic=models.ImageField(blank=True,upload_to="image/",null=True)


class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)  
 
    def total_price(self):
        return self.quantity * self.product.price    