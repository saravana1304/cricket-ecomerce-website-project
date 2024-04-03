from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from userapp1.models import UserProfile
from django.views.decorators.cache import never_cache

# Create your views here.

@never_cache
def userprofile(request):
    if not  request.user.is_authenticated:
        return redirect('home')
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        request.session['user_profile_id'] = user_profile.id
        return render(request,'userprofile/profile.html',{'user_profile': user_profile})


def cart_view(request):
    return render(request,'userprofile/usercart.html')
