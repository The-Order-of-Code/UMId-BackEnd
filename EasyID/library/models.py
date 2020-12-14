from django.db import models
from general.models import User
from django.utils import timezone


class Room(models.Model):
	number = models.IntegerField()
	capacity = models.IntegerField()
	
	def __str__(self):
		return str(self.number)


class Reservation(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	start = models.DateTimeField()
	end = models.DateTimeField()
