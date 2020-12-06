from django.db import models
from django.contrib.auth.models import AbstractUser


class Course(models.Model):
	designation = models.CharField(max_length=45)
	teachingResearchUnits = models.CharField(max_length=45)
	
	def __str__(self):
		return self.designation


class User(AbstractUser):
	fullName = models.CharField(max_length=300)
	birthDate = models.DateField()
	birthParish = models.CharField(max_length=45)
	birthMunicipality = models.CharField(max_length=45)
	birthDistrict = models.CharField(max_length=45)
	birthCountry = models.CharField(max_length=45)

	def __str__(self):
		return self.username


class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
	number = models.IntegerField()
	year = models.IntegerField()
	academicYear = models.IntegerField()
	edition = models.IntegerField()
	specialStatuses = models.CharField(max_length=45)
	studyPlan = models.CharField(max_length=45)
	
	def __str__(self):
		return self.name


class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
