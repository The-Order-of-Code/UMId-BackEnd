from django.contrib import admin
from django.utils.html import format_html
from .models import *
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

    image_tag.short_description = 'Picture'

    list_display = ['username', 'image_tag']

    fieldsets = (
        (None, {
            'fields': ['username', 'password', 'userType', 'fullName', 'birthdate', 'picture']
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': [
                'first_name',
                'last_name',
                'email',
                ('groups', 'user_permissions'),
                ('is_staff', 'is_active', 'is_superuser'),
                ('last_login', 'date_joined'),
            ]
        }),
    )

    def get_changeform_initial_data(self, request):
        return {'birthdate': '2000-01-01'}
