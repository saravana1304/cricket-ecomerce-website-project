from django.shortcuts import render,redirect
from .forms import CreateUserForm,UserLoginForm

# authendication models and functions 

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout

# for managing sessons and user management

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from django.contrib import messages


# Create your views here.

@cache_control(no_cache=True,must_revalidate=True,no_store=True) #performimg the sessions control,not ot redirect to older pages
def userindex(request):
    return render(request,"userapp1/home.html")

def userregister(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userlogin')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    context = {'registerform': form}
    return render(request, "userapp1/register.html", context=context)


def userlogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    return render(request, 'userapp1/login.html', {'loginform': form})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)  #performimg the sessions control,not ot redirect to older pages
@login_required(login_url='userlogin')
def userlogout(request):
    auth.logout(request)
    return redirect('home')


def contactus(request):
    return render(request,'userapp1/contact.html')

def otp(request):
    return render(request,'userapp1/otp.html')

