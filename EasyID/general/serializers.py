from rest_framework import serializers
from django.db import transaction
from .models import *
from library.serializers import ReservationSerializer
from cafeteria.serializers import TicketSerializer

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
            "picture",
        ]


	@transaction.atomic
	def create(self, validated_data):
		#Create user in DB
		userType = validated_data.pop('userType')
		user = User.objects.create(**validated_data)
		user.set_password(user.password)
		user.save()
		return user

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "userType",
            "username",
            "first_name",
            "fullName",
            "birthdate",
            "picture",
        ]


# Course #############################################################################

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


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

        # Create student given the user and course created and also the rest of vars
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
        # Create user in DB
        userData = validated_data.pop('user')
        user = User.objects.create(**userData)

	@transaction.atomic
	def create(self, validated_data):
		#Create user in DB
		userData = validated_data.pop('user')
		user = User.objects.create(**userData)
		user.setEmployee()
		user.is_staff = True
		user.set_password(user.password)
		user.save()

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

class StudentAllSerializer(serializers.Serializer):
	user = StudentSerializer()
	reservations = ReservationSerializer(many=True)
	tickets = TicketSerializer(many=True)

class EmployeeAllSerializer(serializers.Serializer):
	user = EmployeeSerializer()
	reservations = ReservationSerializer(many=True)
	tickets = TicketSerializer(many=True)
