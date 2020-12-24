from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets

from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from django.http.response import JsonResponse, HttpResponse
from django.conf import settings
from datetime import datetime


# Create your views here.

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Ticket.objects.all()
            else:
                return Ticket.objects.all().filter(user=self.request.user)


class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


@api_view(['POST'])
def validateTicket(request):
    # Needs employee sent verification
    # Needs security implemented, only validates payload

    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            payload = data['payload']
            user = payload['user']
            date = payload['date']
            ttype = payload['type']

            if date:
                ticket = Ticket.objects.filter(user=user, date=datetime.today()).first()
            else:
                ticket = Ticket.objects.filter(user=user, type=ttype).first()

            if settings.DEBUG and 'debugdate' in payload:
                ticket = Ticket.objects.filter(user=user, date=payload['debugdate'][:10]).first()
                return JsonResponse(TicketSerializer(ticket).data, status=status.HTTP_200_OK)

            if ticket:
                # log ticket consumption(4 later)
                return HttpResponse(status=status.HTTP_200_OK)
            else:
                return HttpResponse(f'Ticket not found', status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return HttpResponse(f'Field not found: {e.args[0]}', status=status.HTTP_404_NOT_FOUND)
    return HttpResponse('Request is not a POST',status=status.HTTP_501_NOT_IMPLEMENTED)
