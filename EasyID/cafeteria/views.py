from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from pki.PKI.pki import *
from general.views import getUserSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from django.http.response import JsonResponse, HttpResponse
from django.conf import settings
from django.utils import timezone

from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError


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


class TicketLogViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TicketLogSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return TicketLog.objects.all()
            if self.request.user.isEmployee():
                return TicketLog.objects.all().filter(employee=self.request.user)
            else:
                return TicketLog.objects.all().filter(user=self.request.user)


def simpleJsonResponse(detail, status):
    data = {
        'detail': detail
    }
    return JsonResponse(data, status=status)


@transaction.atomic
def moveTicket(ticket, ticketlog):
    with transaction.atomic():
        print('atomic')
        ticket.delete()
        ticketlog.save()


@api_view(['POST'])
def validateTicket(request):
    u = request.user
    if u.is_authenticated:
        if User(id=u.id).isEmployee() or u.is_staff:
            pass
        else:
            return simpleJsonResponse('Not an employee', status=status.HTTP_401_UNAUTHORIZED)
    else:
        return simpleJsonResponse('Not logged in', status=status.HTTP_401_UNAUTHORIZED)

    # Needs security implemented, only validates payload, assumes it's safe
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print("data", data)
        if "token" in data:
            try:
                token = data["token"]
                payld = payload(token)
                username = payld["username"]
                serializer = getUserSerializer(username)
                if serializer is None: return simpleJsonResponse("User type not allowed", status=status.HTTP_401_UNAUTHORIZED)

                #Get user data from serializer
                userDict = json.loads(json.dumps(serializer.data))

                #Validate that the user has permission
                publicKey = userDict["user"]["publicKey"]
                if not validate(publicKey, token): return simpleJsonResponse("Key validation failed", status=status.HTTP_401_UNAUTHORIZED)

                date = payld['date']
                ttypename = payld['type']

                user = User.objects.get(username=username)
                ttype = TicketType.objects.get(name=ttypename)

                if date:
                    ticket = Ticket.objects.filter(user=user, date=timezone.now()).first()
                else:
                    ticket = Ticket.objects.filter(user=user, type=ttype, date=None).first()

                if settings.DEBUG and 'debugdate' in payld:
                    ticket = Ticket.objects.filter(user=user, date=payld['debugdate'][:10]).first()
                    #if ticket:
                        #return JsonResponse(TicketSerializer(ticket).data, status=status.HTTP_200_OK)

                if ticket:
                    tl = TicketLog.fromTicket(ticket=ticket, employee=User.objects.get(id=1), operation='ayyyo')
                    try:
                        moveTicket(ticket, tl)
                    except IntegrityError:
                        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    return HttpResponse(status=status.HTTP_200_OK)
                else:
                    return simpleJsonResponse(f'Ticket not found', status=status.HTTP_404_NOT_FOUND)
            except KeyError as e:
                return simpleJsonResponse(f'Field not found: {e.args[0]}', status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist as e:
                return simpleJsonResponse(fr'User with username {username} not found', status=status.HTTP_404_NOT_FOUND)
            except TicketType.DoesNotExist as e:
                return simpleJsonResponse(fr'TicketType with name {ttypename} not found', status=status.HTTP_404_NOT_FOUND)
    else: return simpleJsonResponse('Request is not a POST', status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def addTickets(request):
    user = request.user
    if not user.is_authenticated:
        return simpleJsonResponse('Not logged in', status=status.HTTP_401_UNAUTHORIZED)

    data = JSONParser().parse(request)
    try:
        username = data['username']
        tickets = data['tickets']
    except KeyError as e:
        return simpleJsonResponse(f'Field not found: {e.args[0]}', status=status.HTTP_404_NOT_FOUND)

    for ticket in tickets:
        try:
            ticketType = ticket['ticketType']
        except KeyError as e:
            return simpleJsonResponse(f'Field not found: {e.args[0]}', status=status.HTTP_404_NOT_FOUND)
        if 'dates' in ticket:
            dates = ticket['dates']
            try:
                ticketType = TicketType.objects.get(name=ticketType)
                for date in dates:
                    user = User.objects.all().get(username=username)
                    tickets_date = Ticket.objects.all().filter(user=user, date=date[:10])
                    print(len(tickets_date))
                    if ((len(tickets_date)+1) > 2):  return simpleJsonResponse(f'Exceeded the number of promotional tickets for that date', status=status.HTTP_406_NOT_ACCEPTABLE)
                    else: 
                        ticket = Ticket(type=ticketType, user=user, date=date[:10])
                        ticket.save()
            except TicketType.DoesNotExist as e:
                return simpleJsonResponse(f'Ticket type: {ticketType}, does not exist', status=status.HTTP_404_NOT_FOUND)
            except ValidationError as e:
                return simpleJsonResponse(f'date: {date} - is invalid. It must be in YYYY-MM-DD format', status=status.HTTP_406_NOT_ACCEPTABLE)

        elif 'amount' in ticket:
            amount = ticket['amount']
            try:
                ticketType = TicketType.objects.get(name=ticketType)
                for i in range(amount):
                    ticket = Ticket(type=ticketType, user=user)
                    ticket.save()
            except TicketType.DoesNotExist as e:
                return simpleJsonResponse(f'Ticket type: {ticketType}, does not exist', status=status.HTTP_404_NOT_FOUND)
        else:
            return simpleJsonResponse('No date or amount specified', status=status.HTTP_404_NOT_FOUND)
    return simpleJsonResponse('Tickets added', status=status.HTTP_200_OK)