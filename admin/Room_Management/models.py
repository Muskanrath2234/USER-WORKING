from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    room_number = models.CharField(max_length=50)
    available_seat = models.IntegerField()
    TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('customized', 'Customized'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    available_date = models.DateField(null=True,blank=True)
    floor = models.IntegerField()

    def __str__(self):
        return self.room_number




