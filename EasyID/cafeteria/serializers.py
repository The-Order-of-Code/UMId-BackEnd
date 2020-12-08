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
	class Meta:
		model = TicketWallet
		fields = "__all__"