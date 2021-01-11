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
import pytz

# Create your views here.

# Room #############################################################################

class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated, IsAdminUser]

def getAvailableRooms(startTime, endTime):
	availableRooms = []
	rooms = Room.objects.all()
	for room in rooms:
		availableTimes = getAvailableTimes(room.id, startTime, endTime)
		if len(availableTimes)>0:
			availableRooms.append(room.id)
	return Room.objects.filter(id__in=availableRooms)

class FreeRoomViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	serializer_class = RoomSerializer
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		startTime = datetime.datetime.now(pytz.utc)
		endTime = startTime + datetime.timedelta(days=1)
		return getAvailableRooms(startTime, endTime)

# Reservation #############################################################################

def getReservations(roomId, startTime, endTime):
	if startTime<endTime:
		roomReservations = Reservation.objects.filter(room=roomId)
		timeReservations = roomReservations.filter(Q(start__lte=endTime) & Q(end__gte=startTime)).order_by("start")
		return timeReservations
	else:
		return None #times don't make sense

def getAvailableTimes(roomId, startTime, endTime, minSpread=5):
	reservations = getReservations(roomId, startTime, endTime)
	if reservations is None: return []
	if len(reservations)==0: return [(startTime, endTime)]
	
	#Add all available time spaces
	time = startTime
	availableTimes = []
	for reservation in reservations:
		if time<reservation.start:
			maxTime = reservation.start - datetime.timedelta(minutes=1)
			if time<maxTime: availableTimes.append((time, maxTime))
		time = reservation.end + datetime.timedelta(minutes=1)
	if time<endTime: availableTimes.append((time, endTime))

	#Remove the time spaces that are too small (smaller than minSpread)
	availableTimesSpread = []
	for (timeFrom, timeTo) in availableTimes:
		timeDiff = timeFrom + datetime.timedelta(minutes=minSpread)
		if timeTo>timeDiff:
			availableTimesSpread.append((timeFrom, timeTo))
	return availableTimesSpread

def reservationAvailable(roomId, startTime, endTime):
	conflictingReservations = getReservations(roomId, startTime, endTime)
	if conflictingReservations is None: return False
	return len(conflictingReservations)==0

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

class FreeTimeViewSet(viewsets.ViewSet):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def list(self, request):
		if "id" in self.request.data:
			roomId = self.request.data["id"]
			startTime = datetime.datetime.now(pytz.utc)
			endTime = startTime + datetime.timedelta(days=1)
			availableTimes = getAvailableTimes(roomId, startTime, endTime)
			#timesDict = {"times": availableTimes}
			return Response(availableTimes)
		else:
			return Response("No room id was sent", status=status.HTTP_400_BAD_REQUEST)

	def create(self, request):
		return self.list(request)