from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework import generics, mixins

# Create your views here.

class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated, IsAdminUser]

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