from django.shortcuts import render
from .models import Room, Reservation
from .serializers import RoomSerializer, RoomInfoSerializer, ReservationSerializer
from rest_framework import viewsets

# Create your views here.

class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer

	def get_serializer_class(self):
		if self.action == "list" or self.action == 'retrieve':
			return RoomInfoSerializer
		else:
			return RoomSerializer

class ReservationViewSet(viewsets.ModelViewSet):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer