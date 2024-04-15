from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from .models import UserProfile
from adminn.models import Category,Product,Brand
from .forms import CreateUserForm
from django.http import JsonResponse
from django.db.models import Q,Min
from django.views.decorators.cache import never_cache
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.db.models import Count



# user index request

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def userindex(request):
    active_categories = Category.objects.filter(is_listed=True)
    active_products = Product.objects.filter(is_listed=True)
    active_brands = Brand.objects.filter(is_listed=True)
    
    lowest_priced_products = {}

    for category in active_categories:
        category_products = active_products.filter(category=category)
        category_products = category_products.filter(brand__in=active_brands)
        
        lowest_priced_product = category_products.aggregate(min_price=Min('selling_price'))
        lowest_price = lowest_priced_product['min_price']
        
        if lowest_price is not None:
            lowest_priced_product = category_products.filter(selling_price=lowest_price).first()
            lowest_priced_products[category] = lowest_priced_product

    context = {
        'categories': active_categories,
        'lowest_priced_products': lowest_priced_products
    }
    return render(request, "userapp1/home.html", context)


# user register page 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
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


# user login page 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def userlogin(request): 
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        userData= User.objects.filter(username=username)
        for user in userData:
            userActive= user.is_active
        if userActive:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                request.session['authenticated']=True
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
        else:
            return JsonResponse({'isBlocked': True})
        
    return render(request, 'userapp1/login.html')


# user log_out page 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)  
@never_cache
@login_required(login_url='userlogin')
def userlogout(request):
    logout(request)
    request.session.flush()
    response = redirect('home')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


# function for genarating otp

def otp(request):
    return render(request,'userapp1/otp.html')


# function for resend otp 

def resendotp(request):
    return render(request,'userapp1/resendotp.html')


# function for contact us page 

def contactus(request):
    return render(request,'userapp1/contact.html')



# function for product deyails 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def product_deatils(request,product_id):
    product=Product.objects.get(pk=product_id)
    similar_products = Product.objects.filter(category=product.category).exclude(pk=product_id)[:4]
    context={
        'product':product,
        'similar_products':similar_products
    }
    return render(request,'userapp1/productdetails.html',context)


# function  for cart_view

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def category_view(request, name):
    try:
        category = Category.objects.get(name=name, is_listed=True)
        products = Product.objects.filter(category=category, is_listed=True, brand__is_listed=True)
        products_count = products.count()
        return render(request, 'userapp1/category.html', {'category': category, 'products': products,'products_count':products_count})
    except Category.DoesNotExist:
        messages.warning(request, 'Category does not exist or is not listed')
        return redirect('category')
