from rest_framework import serializers
from .models import User, Course, Student, Employee

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		#fields = "__all__"
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

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	course = CourseSerializer()

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

class EmployeeSerializer(serializers.ModelSerializer):
	user = UserSerializer()

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