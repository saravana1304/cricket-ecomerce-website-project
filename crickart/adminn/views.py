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
cache_control(no_cache=True,must_revalidate=True,no_store=True)  #performimg the sessions control,not ot redirect to older pages
@login_required(login_url='alogin')
def adminlogout(request):
    auth.logout(request)
    return redirect('alogin')
