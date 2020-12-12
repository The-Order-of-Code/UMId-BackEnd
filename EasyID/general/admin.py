from django.contrib import admin
from django.utils.html import format_html
from .models import User, Student, Employee, Course
from .forms import UserForm

# Register your models here.

# admin.site.register(User)
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Course)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    #form = UserForm

    def image_tag(self, obj):
        return format_html('<img src="{}"width="30" height="30" />'.format(obj.picture.url))

    image_tag.short_description = 'Image'

    list_display = ['username', 'image_tag']


