from django.shortcuts import render
from .models import Ticket, TicketWallet
from .serializers import TicketSerializer, TicketWalletSerializer
from rest_framework import viewsets

# Create your views here.

class TicketViewSet(viewsets.ModelViewSet):
	queryset = Ticket.objects.all()
	serializer_class = TicketSerializer

class TicketWalletViewSet(viewsets.ModelViewSet):
	queryset = TicketWallet.objects.all()
	serializer_class = TicketWalletSerializer