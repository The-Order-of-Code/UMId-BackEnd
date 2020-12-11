from django.shortcuts import render
from .models import User, Course, Student, Employee
from .serializers import UserSerializer, CourseSerializer, StudentSerializer, EmployeeSerializer
from .serializers import UserInfoSerializer, StudentInfoSerializer, EmployeeInfoSerializer
from rest_framework import viewsets

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
	queryset = User.objects.all()

	def get_serializer_class(self):
		if self.action == "list" or self.action == 'retrieve':
			return UserInfoSerializer
		else:
			return UserSerializer

class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer

class StudentViewSet(viewsets.ModelViewSet):
	queryset = Student.objects.all()

	def get_serializer_class(self):
		if self.action == "list" or self.action == 'retrieve':
			return StudentInfoSerializer
		else:
			return StudentSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
	queryset = Employee.objects.all()

	def get_serializer_class(self):
		if self.action == "list" or self.action == 'retrieve':
			return EmployeeInfoSerializer
		else:
			return EmployeeSerializer