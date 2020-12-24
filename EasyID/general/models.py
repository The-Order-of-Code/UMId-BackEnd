from django.db import models
from django.contrib.auth.models import AbstractUser
from general.validators import validate_image_size


class Course(models.Model):
	designation = models.CharField(max_length=45, unique=True)
	teachingResearchUnits = models.CharField(max_length=45)
	
	def __str__(self):
		return self.designation


class User(AbstractUser):
	class UserType(models.TextChoices):
		NONE = "NONE", "NONE"
		STUDENT = "STUDENT", "STUDENT"
		EMPLOYEE = "EMPLOYEE", "EMPLOYEE"

	userType = models.CharField(choices=UserType.choices, default=UserType.NONE, max_length=20)
	fullName = models.CharField(max_length=300)
	birthdate = models.DateField()
	picture = models.ImageField(default='static/defaultAvatar.png', upload_to='profilepictures/', validators=[validate_image_size])
	REQUIRED_FIELDS = ['fullName', 'birthdate']

	REQUIRED_FIELDS = ['birthdate']

	def isStudent(self):
		return self.userType in {self.UserType.STUDENT}

	def setStudent(self):
		self.userType = self.UserType.STUDENT

	def isEmployee(self):
		return self.userType in {self.UserType.EMPLOYEE}

	def setEmployee(self):
		self.userType = self.UserType.EMPLOYEE

	def __str__(self):
		return self.username


class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
	number = models.IntegerField()
	year = models.IntegerField()
	academicYear = models.IntegerField()
	
	def __str__(self):
		return self.user.username


class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
