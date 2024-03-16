from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User as DjangoUser
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User as DjangoUser
from .models import Category
from .views import *


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
 
# user list page
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

# user list update block and unblock
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

# category list page
def category_list(request):
        categories = Category.objects.all()
        return render(request, 'adminn/category.html', {'categories': categories})

#  addcategory page
def add_category(request):
    if request.method=='POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_listed = request.POST.get('is_listed')
        image = request.FILES.get('image')

        if Category.objects.filter(name=name).exists(): 
            error_message= "Category with this name already exists."
            return render(request,'adminn/addcategory.html',{'error_message': error_message})
        
        if Category.objects.filter(description=description).exists():
            error_message= "description is already exists."
            return render(request,'adminn/addcategory.html',{'error_message': error_message})
        
        if not image:
            error_message= "please upload an image."
            return render(request,'adminn/addcategory.html',{'error_message': error_message})

        category = Category(name=name, description=description, is_listed=is_listed, image=image)
        category.save()
        return redirect('categories')
    
    return render(request, 'adminn/addcategory.html')


# update category page
def update_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method=='POST':
            name=request.POST.get('name')
            description = request.POST.get('description')
            is_listed = request.POST.get('is_listed')

            new_image = request.FILES.get('new_image') 
            if new_image:
                category.image=new_image
            
            category.name=name
            category.description=description
            category.is_listed=is_listed
            category.save()
            return redirect('categories')
    return render(request,'adminn/editcategory.html',{'category': category})


def unlist_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'GET':
        if category.is_listed:
            print("2")
            category.is_listed=False
        else:
            category.is_listed=True
        category.save()

        return redirect('categories')
    return redirect('categories')