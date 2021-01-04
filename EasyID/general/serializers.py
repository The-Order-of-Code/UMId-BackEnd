from rest_framework import serializers
from django.db import transaction
from .models import *
from library.serializers import ReservationSerializer
from cafeteria.serializers import TicketSerializer
from django.conf import settings

import base64, uuid
from django.core.files.base import ContentFile
from rest_framework import serializers
import os

# Course #############################################################################

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = "__all__"


# Custom image field - handles base 64 encoded images
class Base64ImageField(serializers.ImageField):
	def to_representation(self, data):
		path = os.path.join(settings.MEDIA_ROOT, str(data))

		with open(path, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read())

		return encoded_string.decode('utf-8')

	def to_internal_value(self, data):
		if isinstance(data, str) and data.startswith('data:image'):
			# base64 encoded image - decode
			format, imgstr = data.split(';base64,') # format ~= data:image/X,
			ext = format.split('/')[-1] # guess file extension
			id = uuid.uuid4()
			data = ContentFile(base64.b64decode(imgstr), name = id.urn[9:] + '.' + ext)
		return super(Base64ImageField, self).to_internal_value(data)

# User #############################################################################


class UserSerializer(serializers.ModelSerializer):
	picture = Base64ImageField()
	class Meta:
		model = User
		fields = [
			"userType",
			"username",
			"password",
			"first_name",
			"fullName",
			"birthdate",
			"picture"]

	@transaction.atomic
	def create(self, validated_data):
		#Create user in DB
		userType = validated_data.pop('userType')
		user = User.objects.create(**validated_data)
		user.set_password(user.password)
		user.save()
		return user

class UserInfoSerializer(serializers.ModelSerializer):
	picture = Base64ImageField()

	class Meta:
		model = User
		fields = [
			"userType",
			"username",
			"first_name",
			"fullName",
			"birthdate",
			"picture"]

# Student #############################################################################

class StudentSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	@transaction.atomic
	def create(self, validated_data):
		#Create user in DB
		userData = validated_data.pop('user')
		user = User.objects.create(**userData)
		user.setStudent()
		user.set_password(user.password)
		user.save()

		#Create student given the user and course created and also the rest of vars
		student = Student.objects.create(user=user, **validated_data)
		return student

	class Meta:
		model = Student
		fields = "__all__"

class StudentInfoSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer()
	course = CourseSerializer()

	class Meta:
		model = Student
		fields = "__all__"

# Employee #############################################################################

class EmployeeSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	@transaction.atomic
	def create(self, validated_data):
		#Create user in DB
		userData = validated_data.pop('user')
		user = User.objects.create(**userData)
		user.setEmployee()
		user.is_staff = True
		user.set_password(user.password)
		user.save()

		#Create employee given the user and the rest of vars
		employee = Employee.objects.create(user=user, **validated_data)
		return employee

	class Meta:
		model = Employee
		fields = "__all__"

class EmployeeInfoSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer()

	class Meta:
		model = Employee
		fields = "__all__"

# All #############################################################################

class StudentAllSerializer(serializers.Serializer):
	user = StudentInfoSerializer()
	reservations = ReservationSerializer(many=True)
	tickets = TicketSerializer(many=True)

class EmployeeAllSerializer(serializers.Serializer):
	user = EmployeeInfoSerializer()
	reservations = ReservationSerializer(many=True)
	tickets = TicketSerializer(many=True)