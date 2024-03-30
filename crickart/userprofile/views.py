from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from userapp1.models import UserProfile

# Create your views here.


def userprofile(request):
    if not  request.user.is_authenticated:
        return redirect('userlogin')
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        return render(request,'userprofile/profile.html',{'user_profile': user_profile})

