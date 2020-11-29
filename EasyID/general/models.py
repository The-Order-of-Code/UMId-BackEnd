from django.db import models

# Create your models here.

class UserType(models.Model):
	designation = models.CharField(max_length=45)
	
	def __str__(self):
		return self.designation

class Course(models.Model):
	designation = models.CharField(max_length=45)
	
	def __str__(self):
		return self.designation

class User(models.Model):
	name = models.CharField(max_length=45)
	number = models.IntegerField()
	username = models.CharField(max_length=45)
	password = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	birthdate = models.DateField()
	#ofAge = models.BooleanField(default=False) #Será necessário ter isto se temos a data de nascimento?
	year = models.IntegerField()
	userType = models.ForeignKey(UserType, null=True, on_delete=models.SET_NULL)
	course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.name