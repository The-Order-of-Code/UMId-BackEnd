from rest_framework import serializers
from django.db import transaction
from .models import User, Course, Student, Employee

#Normal serializer for create, update, etc...
#Info serializer for gets
#Id serializer for inputs that just need a way to identify the object, like when a user makes a reservation
#Maybe find a better way to do this later

# User #############################################################################

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			"username",
			"password",
			"first_name",
			"last_name",
			"fullName",
			"birthDate",
			"birthParish",
			"birthMunicipality",
			"birthDistrict",
			"birthCountry"]

class UserInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			"username",
			"first_name",
			"last_name",
			"fullName",
			"birthDate",
			"birthParish",
			"birthMunicipality",
			"birthDistrict",
			"birthCountry"]

class UserIdSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=45)

# Course #############################################################################

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = "__all__"

class CourseInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = ["designation", "teachingResearchUnits"]

# Student #############################################################################

class StudentSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	course = CourseSerializer()

	@transaction.atomic
	def create(self, validated_data):
		#Create user in DB
		userData = validated_data.pop('user')
		user = User.objects.create(**userData)

		#Create course in DB
		courseData = validated_data.pop('course')
		try:
		    course = Course.objects.get(**courseData)
		except Course.DoesNotExist:
			course = Course.objects.create(**courseData)

		#Create student given the user and course created and also the rest of vars
		student = Student.objects.create(user=user, course=course, **validated_data)
		return student

	class Meta:
		model = Student
		fields = "__all__"

class StudentInfoSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer()
	course = CourseInfoSerializer()

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