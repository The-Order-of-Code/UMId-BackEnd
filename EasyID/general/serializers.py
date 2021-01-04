from rest_framework import serializers
from django.db import transaction
from .models import *
from library.serializers import ReservationSerializer
from cafeteria.serializers import TicketSerializer

# Course #############################################################################

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = "__all__"

# User #############################################################################

class UserSerializer(serializers.ModelSerializer):
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
	picture = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = [
			"userType",
			"username",
			"first_name",
			"fullName",
			"birthdate",
			"picture"]

	def get_picture(self, obj):
		import base64
		import os
		print(obj.picture)
		path = os.path.join('media', str(obj.picture))

		with open(path, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read())

		return encoded_string

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