from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import auth,User
from django.contrib.auth.models import User as DjangoUser
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from userapp1.models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User as DjangoUser


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
        logout(request)
        return redirect('alogin')  # Redirect admin to admin login page:
 

def user_list(request):
    users = DjangoUser.objects.filter(is_superuser=False).order_by('-id')
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_status = request.POST.get('new_status')
        user = DjangoUser.objects.get(id=user_id)
        user.status = new_status
        user.save()
        return redirect('userlist')  # Redirect to the user list page
    return render(request, 'adminn/userlist.html', {'users': users})


def update_status(request, user_id):
    user = get_object_or_404(DjangoUser, id=user_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status == 'blocked':
            user.is_active = False
        elif new_status == 'active':
            user.is_active = True
        user.save()
        return redirect('userlist')  # Redirect to the user list page
    
    return render(request, 'adminn/userlist.html', {'users': DjangoUser.objects.all()})
