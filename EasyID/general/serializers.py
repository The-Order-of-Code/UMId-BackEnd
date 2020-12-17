from rest_framework import serializers
from django.db import transaction
from .models import *
from library.serializers import ReservationSerializer
from cafeteria.serializers import TicketSerializer

#Normal serializer for create, update, etc...
#Info serializer for gets
#Maybe find a better way to do this later

# User #############################################################################

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			"username",
			"password",
			"first_name",
			"fullName",
			"birthdate"]

	@transaction.atomic
	def create(self, validated_data):
		#Create user in DB
		user = User.objects.create(**validated_data)
		user.set_password(user.password)
		user.save()
		return user

class UserInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			"username",
			"first_name",
			"fullName",
			"birthdate"]

# Student #############################################################################

class StudentSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	@transaction.atomic
	def create(self, validated_data):
		#Create user in DB
		userData = validated_data.pop('user')
		user = User.objects.create(**userData)
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

# Course #############################################################################

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = "__all__"

# All #############################################################################

class AllSerializer(serializers.Serializer):
	user = UserSerializer(many=True)
	reservations = ReservationSerializer(many=True)
	tickets = TicketSerializer(many=True)