from django.shortcuts import render
from .models import User, Course, Student
from .serializers import UserSerializer, CourseSerializer, StudentSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer

class StudentViewSet(viewsets.ModelViewSet):
	queryset = Student.objects.all()
	serializer_class = StudentSerializer