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
	number = models.IntegerField()
	birthdate = models.DateField()
	# ofAge = models.BooleanField(default=False) #Será necessário ter isto se temos a data de nascimento?
	year = models.IntegerField()
	course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.name


class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
