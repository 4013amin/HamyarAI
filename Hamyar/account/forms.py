from django import forms
from django.contrib.auth.models import User
from .models import Profile

TAILWIND_INPUT_CLASS = (
    "mt-1 block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 "
    "text-gray-900 focus:border-indigo-500 focus:ring-indigo-500 text-sm outline-none"
)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
            'first_name': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
            'last_name': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        labels = {
            'avatar': 'آواتار جدید',
            'bio': 'درباره من'
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'class': "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"}),
            'bio': forms.Textarea(attrs={'class': TAILWIND_INPUT_CLASS, 'rows': 4, 'placeholder': 'کمی در مورد خودتان بنویسید...'}),
        }