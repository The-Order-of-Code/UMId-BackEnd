from rest_framework import serializers
from .models import Room, Reservation
from general.models import User
from general.serializers import UserIdSerializer

# Room #############################################################################

class RoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = "__all__"

class RoomInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = ["number", "capacity"]

class RoomIdSerializer(serializers.Serializer):
	number = serializers.CharField(max_length=45)

# Reservation #############################################################################

class ReservationSerializer(serializers.ModelSerializer):
	user = UserIdSerializer()
	room = RoomIdSerializer()

	def create(self, validated_data):
		#Get user in DB
		userData = validated_data.pop('user')
		user = User.objects.get(**userData)

		#Get room in DB
		roomData = validated_data.pop('room')
		room = Room.objects.get(**roomData)

		#Create reservation given the user and room and also the rest of vars
		reservation = Reservation.objects.create(user=user, room=room, **validated_data)
		return reservation

	class Meta:
		model = Reservation
		fields = "__all__"