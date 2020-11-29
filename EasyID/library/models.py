from django.db import models
from django.utils import timezone

# Create your models here.

class Room(models.Model):
	number = models.IntegerField()
	capacity = models.IntegerField()
	
	def __str__(self):
		return self.number

class Reservation(models.Model):
	user = models.ForeignKey('general.User', null=True, on_delete=models.CASCADE)
	room = models.ForeignKey(Room, null=True, on_delete=models.CASCADE)
	start = models.DateField()
	end = models.DateField()