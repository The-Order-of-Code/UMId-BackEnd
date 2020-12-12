from rest_framework import serializers
from .models import Ticket, TicketWallet
from general.models import User

# Ticket #############################################################################

class TicketSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ticket
		fields = "__all__"

# TicketWallet #############################################################################

class TicketWalletSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		userId = self.context.get('request', None).user.id
		user = User.objects.get(id=userId)
		ticketWallet = TicketWallet.objects.create(user=user, **validated_data)
		return ticketWallet

	class Meta:
		model = TicketWallet
		fields = ["amount", "ticket"]