from django.db import models
from django.contrib.auth.models import AbstractUser
from general.validators import validate_image_size


class Course(models.Model):
	designation = models.CharField(max_length=45, unique=True)
	teachingResearchUnits = models.CharField(max_length=45)
	
	def __str__(self):
		return self.designation


class User(AbstractUser):
	fullName = models.CharField(max_length=300)
	birthdate = models.DateField()
	picture = models.ImageField(default='static/defaultAvatar.png', upload_to='profilepictures/', validators=[validate_image_size])
	REQUIRED_FIELDS = ['fullName', 'birthdate']

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
