from django.shortcuts import render
from .models import User, Course, Student, Employee
from library.models import Reservation
from cafeteria.models import TicketWallet
from pki.pki import getUserHashCertificate
from .serializers import UserSerializer, CourseSerializer, StudentSerializer, EmployeeSerializer, AllSerializer
from .serializers import UserInfoSerializer, StudentInfoSerializer, EmployeeInfoSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from collections import namedtuple
import json

# Create your views here.

""" Exemplo Student POST:
{
	"user": {
		"portrait": "", 
		"username": "",
		"password": "",
		"firstName": "",
		"fullName": "",
		"birthDate": ""
	},
	"course": {
		"designation": "",
		"teachingResearchUnits": ""
	}
	"number": null,
	"year": null,
	"academicYear": null
	}
}
"""

class UserViewSet(viewsets.ModelViewSet):
	def get_serializer_class(self):
		if self.action == "list" or self.action == "retrieve":
			return UserInfoSerializer
		else:
			return UserSerializer

	def get_queryset(self):
		if self.request.user.is_authenticated:
			if self.request.user.is_superuser:
				return User.objects.all()
			else:
				return User.objects.all().filter(id=self.request.user.id)

class StudentViewSet(viewsets.ModelViewSet):
	def get_serializer_class(self):
		if self.action == "list" or self.action == "retrieve":
			return StudentInfoSerializer
		else:
			return StudentSerializer

	def get_queryset(self):
		if self.request.user.is_authenticated:
			if self.request.user.is_superuser:
				return Student.objects.all()
			else:
				return Student.objects.all().filter(id=self.request.user.id)

class EmployeeViewSet(viewsets.ModelViewSet):
	queryset = Employee.objects.all()
	#Remove comments after testing, this is just to create admins easily
	#authentication_classes = [SessionAuthentication, BasicAuthentication]
	#permission_classes = [IsAuthenticated, IsAdminUser]
	
	def get_serializer_class(self):
		if self.action == "list" or self.action == "retrieve":
			return EmployeeInfoSerializer
		else:
			return EmployeeSerializer

class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated, IsAdminUser]


# All ################################################################################################################


Attributes = namedtuple("Attributes", ("user", "reservations", "ticketWallet"))

class AllViewSet(viewsets.ViewSet):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def list(self, request):
		if "csr" in self.request.data:
			attributes = Attributes(
				user=User.objects.all().filter(username=self.request.user.username),
				reservations=Reservation.objects.all().filter(user=self.request.user),
				ticketWallet=TicketWallet.objects.all().filter(user=self.request.user)
			)
			serializer = AllSerializer(attributes)

			userDict = json.loads(json.dumps(serializer.data))["user"][0]
			csr = self.request.data["csr"]
			(userHash, userCertificate) = getUserHashCertificate(userDict, csr)

			serializerCsr = {"userHash": userHash, "userCertificate": userCertificate}
			serializerCsr.update(serializer.data)
			return Response(serializerCsr)

		return Response("No CSR data found", status=status.HTTP_400_BAD_REQUEST)