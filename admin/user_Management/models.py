from django.db import models
from django.contrib.auth.models import User

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    room_number = models.CharField(max_length=10)
    bed_number = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    aadhar_card = models.CharField(max_length=12, null=True, blank=True)
    pan_card = models.CharField(max_length=10, null=True, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
