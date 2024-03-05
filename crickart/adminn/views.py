from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import auth

# for performing sessions
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

# Create your views here.

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='alogin')
def ahome(request):
    return render(request, 'adminn/home.html')

#admin login request 
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                # Log in the user
                login(request, user)
                return redirect('ahome')
    return render(request, 'adminn/login.html')


# admin logout request
@login_required(login_url='alogin')
def adminlogout(request):
    # Check if the user is an admin before logging out
    if request.user.is_superuser:
        auth.logout(request)
        return redirect('alogin')  # Redirect admin to admin login page
    else:
        # If the user is not an admin, redirect them to the user home page
        return redirect('ahome')