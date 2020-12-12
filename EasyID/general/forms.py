from django import forms
from .models import User
from django.utils.html import format_html


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'picture', ]

