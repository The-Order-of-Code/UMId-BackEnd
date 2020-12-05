from rest_framework import serializers
from .models import User, Course, Student

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		#fields = "__all__"
		fields = ["username", "password"]

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
		fields = ["user", "course", "number", "birthdate", "year"]