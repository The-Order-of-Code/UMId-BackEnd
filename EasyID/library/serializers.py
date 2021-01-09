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
	def create(self, validated_data):
		user = validated_data.pop('user', None)
		userId = self.context.get('request', None).user.id
		user = User.objects.get(id=userId)
		reservation = Reservation.objects.create(user=user, **validated_data)
		return reservation

	class Meta:
		model = Reservation
		fields = "__all__"