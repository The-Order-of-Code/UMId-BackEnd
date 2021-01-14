from django.shortcuts import render
from .models import *
from library.models import Reservation
from cafeteria.models import Ticket
from pki.PKI.pki import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics, mixins
from collections import namedtuple
import json

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

def getUserSerializer(username):
	user = User.objects.all().get(username=username)
	if user.isStudent():
		user = Student.objects.all().get(user=user)
		return StudentInfoSerializer(user)
	elif user.isEmployee():
		user = Employee.objects.all().get(user=user)
		return EmployeeInfoSerializer(user)
	else:
		return None

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

def savePublicKey(username, publicKey):
	user = User.objects.all().get(username=username)
	user.setPublicKey(publicKey)
	user.save()

class AllViewSet(viewsets.ViewSet):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def list(self, request):
		if "csr" in self.request.data:
			#Get arguments
			username = self.request.user.username
			csr = self.request.data["csr"]

			#Get user and send data to serializer of its type
			serializer = getUserSerializer(username)
			if serializer is None: return Response("User type not allowed", status=status.HTTP_401_UNAUTHORIZED)

			#Get user data from serializer, get hash/certificate/publicKey and save publicKey
			userDict = json.loads(json.dumps(serializer.data))
			(userHash, userCertificate, userPublicKey) = getUserHashCertificate(userDict, csr)
			savePublicKey(username, userPublicKey)

			#Get user and everything else and send data to serializer of its type
			serializer = getUserAllSerializer(username)
			if serializer is None: return Response("User type not allowed", status=status.HTTP_401_UNAUTHORIZED)

			#Add hash/certificate to serializer data and send response
			serializerCsr = {"mso": userHash, "userCertificate": userCertificate}
			
			userInfo = json.loads(json.dumps(serializer.data))
			(userInfo["user"])["user"].pop("publicKey")
			serializerCsr.update(userInfo)
			return Response(serializerCsr)
		else:
			return Response("No CSR data found", status=status.HTTP_400_BAD_REQUEST)

	def create(self, request):
		return self.list(request)

def getUserAttributes(userDict, attributes):
	#Format attributes
	attributesDict = {}
	for attribute in attributes:
		if len(attribute.split("."))==2:
			[model, modelAttribute] = attribute.split(".")
			if model in userDict and modelAttribute in userDict[model]:
				attributesDict[attribute] = userDict[model][modelAttribute]
			else:
				attributesDict[attribute] = None
		elif attribute in userDict["user"]:
			attributesDict[attribute] = userDict["user"][attribute]
		elif attribute in userDict:
			attributesDict[attribute] = userDict[attribute]
		else:
			attributesDict[attribute] = None
	return attributesDict

class AttributesViewSet(viewsets.ViewSet):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated, IsAdminUser]

	def list(self, request):
		if "token" in self.request.data:
			#Get arguments
			token = self.request.data["token"]
			data = payload(token)
			username = data["username"]
			attributes = data["namespaces"]
			#Get user and send data to serializer of its type
			serializer = getUserSerializer(username)
			if serializer is None: return Response("User type not allowed", status=status.HTTP_401_UNAUTHORIZED)

			#Get user data from serializer
			userDict = json.loads(json.dumps(serializer.data))

			#Validate that the user has permission
			publicKey = userDict["user"]["publicKey"]
			if not validate(publicKey, token): return Response("Key validation failed", status=status.HTTP_401_UNAUTHORIZED)

			#Get attributes that were asked
			attributesDict = getUserAttributes(userDict, attributes)
			return Response(attributesDict)
		else:
			return Response("No token was sent", status=status.HTTP_400_BAD_REQUEST)

	def create(self, request):
		return self.list(request)