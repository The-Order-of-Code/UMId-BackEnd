#Setup a new Django project
#Edit settings.py however you want
#For Windows remove first #! line inside manage.py
"py D:/Python/Scripts/django-admin.py startproject <project name>"

#Create database or execute operations (from makemigrations below)
"py manage.py migrate"

#Create user
"py manage.py createsuperuser"

#Create app
#Add app to settings after, like INSTALLED_APPS = ['<app name>', ...]
"py manage.py startapp <app name>"

#Create operations for database
#Created models are transformed into operations
"py manage.py makemigrations"

#Run server
"py manage.py runserver"

#Call operations on models on database
"py manage.py shell"

#For example:
#from <app name>.models import <class name>
#x = <class name>.objects.get(...)
#x = <class name>(<attribute name> = ..., ...)
#x.<attribute name> = ...
#x.save()
#x.delete()

#For N to N:
#x = <class name>(<attribute name> = ..., ...)
#y = <class name>(<attribute name> = ..., ...)
#x.<y attribute name>.add(y)
#Or
#x = <class name>(<attribute name> = ..., ...)
#y = x.<y attribute name>.create(<attribute name> = ..., ...)

#To get list of each N:
#x.<y attribute name>.all()
#y.<x class name>_set.all()

#To filter:
#<x class name>.objects.filter(<y attribute name>__<attribute name>__startswith = ...)
#<y class name>.objects.filter(<x class name>__<attribute name>__startswith = ...)

#REST:
#from appTest.serializers import CharacterSerializer
#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser

#x = <x class name>.objects.get(...)
#serializer = CharacterSerializer(x)
#Also
#serializer = CharacterSerializer(Character.objects.all(), many=True)

#serializer.data
#json = JSONRenderer().render(serializer.data)