# accounts/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Profile

TAILWIND_INPUT_CLASS = (
    "mt-1 block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 "
    "text-gray-900 focus:border-indigo-500 focus:ring-indigo-500 text-sm outline-none"
)

class CustomLoginForm(forms.Form):
    username = forms.CharField(label="نام کاربری", widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}))
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class': TAILWIND_INPUT_CLASS}))

class CustomRegisterForm(forms.Form):
    username = forms.CharField(label="نام کاربری", widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASS}))
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class': TAILWIND_INPUT_CLASS}))
    password_confirm = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput(attrs={'class': TAILWIND_INPUT_CLASS}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری قبلاً انتخاب شده است.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("رمزهای عبور با هم مطابقت ندارند.")
        return cleaned_data

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