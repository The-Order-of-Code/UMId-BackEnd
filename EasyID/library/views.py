from django.shortcuts import render
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer
from rest_framework import viewsets

# Create your views here.

class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer

class ReservationViewSet(viewsets.ModelViewSet):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer