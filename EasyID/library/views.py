from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics, mixins
from rest_framework import status
from django.db.models import Q
import datetime

# Create your views here.

# Room #############################################################################

class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated, IsAdminUser]

# Reservation #############################################################################

def reservationAvailable(roomId, startTime, endTime):
	roomReservations = Reservation.objects.filter(room=roomId)
	conflictingReservations = roomReservations.filter(Q(start__lte=endTime) & Q(end__gte=startTime))
	return startTime<endTime and len(conflictingReservations)==0

class ReservationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
												  mixins.CreateModelMixin,
												  mixins.RetrieveModelMixin,
												  mixins.DestroyModelMixin):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		if self.request.user.is_authenticated:
			if self.request.user.is_staff:
				return Reservation.objects.all()
			else:
				return Reservation.objects.all().filter(user=self.request.user)

	def create(self, request, *args,**kwargs):
		room = self.request.data["room"]
		start = self.request.data["start"]
		end = self.request.data["end"]
		if reservationAvailable(room, start, end):
			return super(ReservationViewSet, self).create(request, *args,**kwargs)
		else:
			return Response("Reservation time not available", status=status.HTTP_400_BAD_REQUEST)