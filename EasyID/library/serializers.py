from rest_framework import serializers
from .models import *
from general.models import User

# Room #############################################################################

class RoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = "__all__"

# Reservation #############################################################################

class ReservationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reservation
		fields = "__all__"