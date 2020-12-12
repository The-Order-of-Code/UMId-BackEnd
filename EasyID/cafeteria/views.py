from django.shortcuts import render
from .models import Ticket, TicketWallet
from .serializers import TicketSerializer, TicketWalletSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets

# Create your views here.

class TicketViewSet(viewsets.ModelViewSet):
	queryset = Ticket.objects.all()
	serializer_class = TicketSerializer
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated, IsAdminUser]

class TicketWalletViewSet(viewsets.ModelViewSet):
	queryset = TicketWallet.objects.all()
	serializer_class = TicketWalletSerializer
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		if self.request.user.is_authenticated:
			if self.request.user.is_superuser:
				return TicketWallet.objects.all()
			else:
				return TicketWallet.objects.all().filter(user=self.request.user)