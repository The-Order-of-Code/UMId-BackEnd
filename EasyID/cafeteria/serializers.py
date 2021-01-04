from rest_framework import serializers
from .models import *
from general.models import User

# Ticket #############################################################################


class TicketSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		username = self.context.get('request', None).user.username
		user = User.objects.get(username=username)
		ticket = Ticket.objects.create(user=user, **validated_data)
		return ticket

	class Meta:
		model = Ticket
		fields = ["type", "code", "date", "hash"]

# TicketType #############################################################################


class TicketTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = TicketType
		fields = "__all__"

# Profile #############################################################################


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = "__all__"

# TicketLog #############################################################################


class TicketLogSerializer(serializers.ModelSerializer):
	user = serializers.SlugRelatedField(read_only=True, slug_field='username')
	type = serializers.SlugRelatedField(read_only=True, slug_field='name')

	class Meta:
		model = TicketLog
		fields = ['user', 'type', 'consumed']
