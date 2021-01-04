from django.shortcuts import render
from .models import *
from library.models import Reservation
from cafeteria.models import Ticket
from pki.pki import getUserHashCertificate
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics, mixins
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

class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
										   mixins.CreateModelMixin,
										   mixins.RetrieveModelMixin):
	def get_serializer_class(self):
		if self.action == "list" or self.action == "retrieve":
			return UserInfoSerializer
		elif self.action == "create":
			return UserSerializer

	def get_queryset(self):
		if self.request.user.is_authenticated:
			if self.request.user.is_staff:
				return User.objects.all()
			else:
				return User.objects.all().filter(username=self.request.user.username)

class StudentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
											  mixins.CreateModelMixin,
											  mixins.RetrieveModelMixin):
	def get_serializer_class(self):
		if self.action == "list" or self.action == "retrieve":
			return StudentInfoSerializer
		elif self.action == "create":
			return StudentSerializer

	def get_queryset(self):
		if self.request.user.is_authenticated:
			if self.request.user.is_staff:
				return Student.objects.all()
			else:
				return Student.objects.all().filter(username=self.request.username)

class EmployeeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
											   mixins.CreateModelMixin,
											   mixins.RetrieveModelMixin):
	queryset = Employee.objects.all()
	#Remove comments after testing, this is just to create admins easily
	#authentication_classes = [SessionAuthentication, BasicAuthentication]
	#permission_classes = [IsAuthenticated, IsAdminUser]
	
	def get_serializer_class(self):
		if self.action == "list" or self.action == "retrieve":
			return EmployeeInfoSerializer
		elif self.action == "create":
			return EmployeeSerializer

class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated, IsAdminUser]


# All ################################################################################################################


Attributes = namedtuple("Attributes", ("user", "reservations", "tickets"))

def getUserAllSerializer(username):
	user = User.objects.all().get(username=username)
	if user.isStudent():
		attributes = Attributes(
			user=Student.objects.all().get(user=user),
			reservations=Reservation.objects.all().filter(user=user),
			tickets=Ticket.objects.all().filter(user=user)
		)
		return StudentAllSerializer(attributes)
	elif user.isEmployee():
		attributes = Attributes(
			user=Employee.objects.all().get(user=user),
			reservations=Reservation.objects.all().filter(user=user),
			tickets=Ticket.objects.all().filter(user=user)
		)
		return EmployeeAllSerializer(attributes)
	else:
		return None

class AllViewSet(viewsets.ViewSet):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def list(self, request):
		if "csr" in self.request.data:
			#Get user and send data to serializer of its type
			username = self.request.user.username
			serializer = getUserAllSerializer(username)
			if serializer is None: return Response("User type not allowed", status=status.HTTP_401_UNAUTHORIZED)

			#Get user data from serializer and get check hash/certificate
			userDict = json.loads(json.dumps(serializer.data))["user"]
			csr = self.request.data["csr"]
			(userHash, userCertificate) = getUserHashCertificate(userDict, csr)

			#Add hash/certificate to serializer data and send response
			serializerCsr = {"userHash": userHash, "userCertificate": userCertificate}
			serializerCsr.update(serializer.data)
			return Response(serializerCsr)
		else:
			return Response("No CSR data found", status=status.HTTP_400_BAD_REQUEST)

	def create(self, request):
		return self.list(request)

class AttributesViewSet(viewsets.ViewSet):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated, IsAdminUser]

	def list(self, request):
		if "username" in self.request.data and "namespaces" in self.request.data:
			#Get user and send data to serializer of its type
			username = self.request.data["username"]
			serializer = getUserAllSerializer(username)
			if serializer is None: Response("User type not allowed", status=status.HTTP_401_UNAUTHORIZED)

			#Get user data from serializer
			userDict = json.loads(json.dumps(serializer.data))["user"]

			attributes = self.request.data["namespaces"]
			attributesDict = {}
			for attribute in attributes:
				if len(attribute.split("."))==2:
					[model, modelAttribute] = attribute.split(".")
					if modelAttribute in userDict[model]:
						attributesDict[attribute] = userDict[model][modelAttribute]
				elif attribute in userDict["user"]:
					attributesDict[attribute] = userDict["user"][attribute]
				elif attribute in userDict:
					attributesDict[attribute] = userDict[attribute]
				else:
					attributesDict[attribute] = None

			return Response(attributesDict)
		else:
			return Response("No username/namespaces were sent", status=status.HTTP_400_BAD_REQUEST)

	def create(self, request):
		return self.list(request)

def getUserAttributes(username, attributes):
	#Get user and send data to serializer of its type
	serializer = getUserAllSerializer(username)
	if serializer is None: return None

	#Get user data from serializer
	userDict = json.loads(json.dumps(serializer.data))["user"]

	attributesDict = {}
	for attribute in attributes:
		if len(attribute.split("."))==2:
			[model, modelAttribute] = attribute.split(".")
			if modelAttribute in userDict[model]:
				attributesDict[attribute] = userDict[model][modelAttribute]
		elif attribute in userDict["user"]:
			attributesDict[attribute] = userDict["user"][attribute]
		elif attribute in userDict:
			attributesDict[attribute] = userDict[attribute]
		else:
			attributesDict[attribute] = None

	return attributesDict