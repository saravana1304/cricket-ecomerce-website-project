from django.shortcuts import render,redirect
from .forms import CreateUserForm,UserLoginForm

# authendication models and functions 

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout


# Create your views here.


def userindex(request):
    return render(request,"userapp1/home.html")



def userregister(request):
    form=CreateUserForm()
    print(request)
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userlogin')
    context={'registerform':form}
    return render(request,"userapp1/register.html",context=context)



def userlogin(request):
    form=UserLoginForm()
    if request.method=='POST':
        form=UserLoginForm(request,data=request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('home')
    context={'loginform':form}
    return render(request,'userapp1/login.html',context=context)


def contactus(request):
    return render(request,'userapp1/contact.html')

