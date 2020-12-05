from django.db import models
from django.contrib.auth.models import AbstractUser


class UserType(models.Model):
	designation = models.CharField(max_length=45)
	
	def __str__(self):
		return self.designation


class Course(models.Model):
	designation = models.CharField(max_length=45)
	
	def __str__(self):
		return self.designation


class User(AbstractUser):
	pass

	def __str__(self):
		return self.username


class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
	number = models.IntegerField()
	birthdate = models.DateField()
	year = models.IntegerField()
	
	def __str__(self):
		return self.name


class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
