from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import  CustomLoginForm , CustomRegisterForm , ProfileUpdateForm , UserUpdateForm
from . import models


# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return  redirect('login')
    
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            models.User.objects.create_user(
                username= username,
                password=password
            )
            messages.success(request, 'ثبت‌نام شما با موفقیت انجام شد. اکنون می‌توانید وارد شوید.')
            return redirect('login')
    else:
        form = CustomRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid:
            username = form.cleaned_data.get('username')
            password = form.changed_data.get('password')
            user = authenticate(request , username=username , password=password)
            if user is not None:
                login(request , user)
                messages.success(request, f'خوش آمدید، {username}!')
                return redirect('profile')
            else:
                messages.error(request , 'نام کاربری یا رمز عبور اشتباه است.')

        else:
            form = CustomLoginForm()

        return render(request, 'accounts/login.html', {'form': form})
    
@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'پروفایل شما با موفقیت بروزرسانی شد!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, "شما با موفقیت از حساب خود خارج شدید.")
    return redirect('login')