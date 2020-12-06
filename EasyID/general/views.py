from django.shortcuts import render
from .models import User, Course, Student
from .serializers import UserSerializer, CourseSerializer, StudentSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

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
	serializer_class = UserSerializer

class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer

class StudentViewSet(viewsets.ModelViewSet):
	queryset = Student.objects.all()
	serializer_class = StudentSerializer