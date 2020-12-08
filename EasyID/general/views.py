from django.shortcuts import render
from .models import User, Course, Student, Employee
from .serializers import UserSerializer, CourseSerializer, StudentSerializer, EmployeeSerializer
from .serializers import UserInfoSerializer, StudentInfoSerializer, EmployeeInfoSerializer
from rest_framework import viewsets

# Create your views here.

""" Exemplo Student POST:
{
	"user": {
		"username": "pedrohpf",
		"password": "1234",
		"first_name": "Pedro",
		"last_name": "Ferreira",
		"fullName": "Pedro Henrique de Passos Ferreira",
		"birthDate": "2020-12-06",
		"birthParish": "c",
		"birthMunicipality": "idk",
		"birthDistrict": "huh",
		"birthCountry": "Portugal"
	},
	"course": {
		"id": 1,
		"designation": "Mestrado Integrado em Engenharia Informática",
		"teachingResearchUnits": "Escola de Engenharia"
	},
	"number": 81403,
	"year": 5,
	"academicYear": 2020,
	"edition": 13,
	"specialStatuses": "Finalista",
	"studyPlan": "M002"
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