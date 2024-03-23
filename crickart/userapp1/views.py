from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from .models import UserProfile
from adminn.models import Category
from .forms import CreateUserForm,AuthenticationForm
from django.http import JsonResponse


# Create your views here.

@cache_control(no_cache=True,must_revalidate=True,no_store=True) #performimg the sessions control,not ot redirect to older pages
def userindex(request):
    categories=Category.objects.all().exclude(is_listed=False)
    context={'categories': categories}
    return render(request,"userapp1/home.html",context)


def userregister(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Check if a UserProfile already exists for the user
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            # Update additional fields in the existing UserProfile
            user_profile.phone_number = form.cleaned_data['phone_number']
            user_profile.place = form.cleaned_data['place']
            user_profile.save()
            return redirect('userlogin')
        else:
            # Add form errors to the messages framework
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    context = {'registerform': form}
    return render(request, "userapp1/register.html", context=context)


@ensure_csrf_cookie
def userlogin(request):  
    if request.method=='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        userData= User.objects.filter(username=username)
        for i in userData:
            userActive= i.is_active
        if userActive:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
        else:
            return JsonResponse({'isBlocked': True})
        
    return render(request, 'userapp1/login.html')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)  #performimg the sessions control,not ot redirect to older pages
@login_required(login_url='userlogin')
def userlogout(request):
    logout(request)
    return redirect('home')


def otp(request):
    return render(request,'userapp1/otp.html')


def resendotp(request):
    return render(request,'userapp1/resendotp.html')



def contactus(request):
    return render(request,'userapp1/contact.html')
