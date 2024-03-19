from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from .models import UserProfile
from adminn.models import Category
from django.contrib.auth.models import auth
from django.contrib.auth.forms import AuthenticationForm

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


def userlogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    print('1')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print('2')
        print(form.is_valid())

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        print('username: '+username)
        print('password: '+password)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            print(user.is_active)
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'userapp1/blocked.html')
        else:
            messages.error(request, "Invalid username or password")
            print('4')

    else:
        form = AuthenticationForm(request)  
    print(6)  
    return render(request, 'userapp1/login.html', {'loginform': form})



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
