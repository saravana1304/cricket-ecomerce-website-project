from django.shortcuts import render,HttpResponse

# Create your views here.


def index(request):
    return render(request,"userapp1/home.html")

def register(request):
    return render(request,"userapp1/register.html")

