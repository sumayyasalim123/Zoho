from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from star_ratings.models import Rating
from django.conf import settings


class CustomUser(AbstractUser):
     user_type = models.CharField(default=1, max_length=10,null=True)

class Usermember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    c_number = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    profilepic = models.ImageField(blank=True, upload_to="image/", null=True)
    confirmation_code = models.CharField(max_length=6, null=True, blank=True)
    status = models.CharField(max_length=1, default='1',null=True)
def __str__(self):
        return self.user.username
    

class Categories(models.Model):
    category_name = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=10, default='1', null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_categories',null=True)

    created_by_type = models.CharField(max_length=10, default='1', null=True)  # New field
    def __str__(self):
        return self.category_name

class UserMember1(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
   
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    a_ddress = models.CharField(max_length=255,null=True)
    contactnumber = models.CharField(max_length=255,null=True)
    experience = models.CharField(default=1, max_length=25,null=True)
    dob = models.DateField(null=True, blank=True)

    
    id_type = models.CharField(max_length=255,null=True)
    profile_picture = models.ImageField(upload_to="images/", null=True, blank=True)
    certificate = models.FileField(upload_to="certificates/", null=True, blank=True)

    STATUS_CHOICES = [
        ('1', 'Pending'),
        ('2', 'Approved'),
        ('3', 'Rejected'),
    ]

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')


class DurationField(models.CharField):
    description = "Custom duration field"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 20)
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        try:
            # Validate the duration format
            hours_str, minutes_str = value.split('hr ')
            hours = int(hours_str)
            minutes = int(minutes_str.split('min')[0])
            if hours < 0 or minutes < 0:
                raise ValidationError("Duration cannot be negative")
        except (ValueError, IndexError):
            raise ValidationError("Invalid duration format. Use 'Xhr Ymin' format.")

    def to_python(self, value):
        if value is None:
            return value
        try:
            hours_str, minutes_str = value.split('hr ')
            hours = int(hours_str)
            minutes = int(minutes_str.split('min')[0])
            return hours * 60 + minutes  # Convert to total minutes
        except (ValueError, IndexError):
            return value

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        return str(value) if value is not None else None



class Service(models.Model):
     added_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
     categories = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
     title=models.CharField(max_length=255,null=True)
     image=models.ImageField(upload_to="images/", null=True, blank=True)
     description=models.CharField(max_length=255,null=True)
     price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
     duration = DurationField(null=True)
     def get_duration_display(self):
        if self.duration is not None:
            hours = self.duration // 60
            minutes = self.duration % 60
            return f"{hours}hr {minutes}min"
        return None
     STATUS_CHOICES = [
        ('1', 'Pending'),
        ('2', 'Approved'),
        ('3', 'Rejected'),
    ]

     status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')


class Booking(models.Model):
    STATUS_CHOICES = [
        ('1', 'Pending'),
        ('2', 'Approved'),
        ('3', 'Rejected'),
    ]

    user = models.ForeignKey(Usermember, on_delete=models.CASCADE,null=True) 
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='worker_bookings', null=True)

    service = models.ForeignKey(Service, on_delete=models.CASCADE ,null=True)
    date_of_booking = models.DateTimeField(auto_now_add=True ,null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1',null=True)
    worker_approval=models.CharField(max_length=3,  default='1',null=True)
    task_compleated=models.CharField(max_length=2,  default='1',null=True)
    


class Review(models.Model):
    
    rating = models.IntegerField(blank=True, null=True)  # Assuming Rating is an integer field
    comments = models.TextField(blank=True, null=True)
    bookings = models.ForeignKey(Booking, on_delete=models.CASCADE ,null=True)
    
    

    
    
    

    

        








         