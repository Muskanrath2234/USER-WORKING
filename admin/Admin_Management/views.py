from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import random
from django.contrib.auth.models import User
from django.shortcuts import redirect

@csrf_exempt
def verifyOPT(request):
    if request.method == 'POST':
        useropt = request.POST.get('otp')
        original_otp = request.POST.get('original_otp')  # OTP sent via email
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Verify OTP and passwords
        if useropt == original_otp:
            if password1 == password2:
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                # Return success response
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Passwords do not match'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid OTP'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



def home(request):
    return render(request,'home.html') 
def budget(request):
    return render(request,'budget.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                auth_login(request, user)
                messages.info(request, f'{username}, You are logged in.')
                return redirect('home')  # Replace 'home' with the actual name of your home view
            else:
                messages.info(request, 'You do not have permission to access this page.')
                return redirect('admin_login')
        else:
            messages.info(request, 'Wrong password or username')
            return redirect('admin_login')
    return render(request, 'login.html')




           

def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            otp = random.randint(100000, 999999)

            messages.success(request, 'Registration successful! Please verify your email.')
            send_mail(
                "User Data",
                f"Verify your email using the OTP: \n {otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=True
            )

            # Render the verify page with the OTP and user details for verification
            return render(request, 'verify.html', context={
                'otp': otp,
                'username': username,
                'email': email,
                'password1': password1,
                'password2': password2
            })

            # form.save() and redirect won't be executed because it's after a return statement

        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'register.html', {'form': form})

    else:
        form = CreateUserForm()

    return render(request, 'register.html', {'form': form})

 
            


def view_all_users(request):
   users = User.objects.all()
   return render(request,'view_all_users.html',{'users':users})

def user_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required
def view_profile(request):
    user = request.user
    return render(request, 'view_profile.html', {'user': user})


@login_required(login_url='admin_login')
def editprofile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            username = request.user.username
            messages.success(request, f'{username}, Your profile is updated.')
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    context = {'form': form}
    return render(request, 'editprofile.html', context)





def user_logout(request):
    logout(request)
    return redirect('admin_login')