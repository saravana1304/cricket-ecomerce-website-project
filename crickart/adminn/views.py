from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User as DjangoUser
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User as DjangoUser
from .models import Category,Brand,Product
from userprofile.models import Order
from .views import *
from django.views.decorators.cache import never_cache
from django.http import JsonResponse


# Decorator to check if the user is a superuser

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('alogin')  
        return view_func(request, *args, **kwargs)
    return wrapper


# function for admin home page request

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='alogin')
def ahome(request):
    return render(request, 'adminn/home.html')

# function for admin login request 

@never_cache
def adminlogin(request):
    if request.user.is_superuser:
        return redirect('ahome')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                # Log in the user
                login(request, user)
                request.session['authenticated']=True
                return redirect('ahome')
    return render(request, 'adminn/login.html')


# function for admin logout request

@login_required(login_url='alogin')
def adminlogout(request):
    # Check if the user is an admin before logging out
    if request.user.is_superuser:
        logout(request)
        request.session.flush()
        return redirect('alogin')  # Redirect admin to admin login page:
 
# function for user list page

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='alogin')
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


# function for user list update block and unblock

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
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


# function for category list page

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='alogin')
def category_list(request):
        categories = Category.objects.all()
        return render(request, 'adminn/category.html', {'categories': categories})


# function for addcategory page

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
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


# function for update category page

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
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


# function for unlist category from admin side 

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def unlist_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'GET':
        if category.is_listed:
            category.is_listed=False
        else:
            category.is_listed=True
        category.save()

        return redirect('categories')
    return redirect('categories')


# function for Brand list page

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='alogin')
def brand_list(request):
        brand = Brand.objects.all()
        return render(request, 'adminn/brand.html', {'brand': brand})


# function for Add brand for our site

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_brand(request):
    if request.method=='POST':
        name = request.POST.get('name')
        is_listed = request.POST.get('is_listed')

        if Brand.objects.filter(name=name).exists(): 
            error_message= "Brand with this name already exists."
            return render(request,'adminn/addbrand.html',{'error_message': error_message})
        
        brand = Brand(name=name, is_listed=is_listed,)
        brand.save()
        return redirect('brandlist')
    return render(request, 'adminn/addbrand.html')


# function for update brand for our site

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def update_brand(request, brand_id):
    brands = get_object_or_404(Brand, pk=brand_id)
    if request.method=='POST':
            name=request.POST.get('name')
            is_listed = request.POST.get('is_listed')
            brands.name=name
            brands.is_listed=is_listed
            brands.save()
            return redirect('brandlist')
    return render(request,'adminn/editbrand.html',{'brand': brands})


# function for edit brand for our site

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def unlist_brand(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)
    if request.method == 'GET':
        if brand.is_listed:
            brand.is_listed=False
        else:
            brand.is_listed=True
        brand.save()
        return redirect('brandlist')
    return redirect('brandlist')


# function for products list page:

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='alogin')
def product_list(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()
    return render(request, 'adminn/product.html', {'categories': categories, 'brands': brands,'products':products})
    

# function for Add product page:

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_product(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    if request.method=='POST':
        product_name=request.POST.get('product_name')
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')
        description=request.POST.get('description')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        stock = request.POST.get('stock')
        landing_price = request.POST.get('landing_price')
        selling_price = request.POST.get('selling_price')
        is_listed =  request.POST.get('is_listed')

        category_instance = Category.objects.get(id=category_id)
        brand_instance = Brand.objects.get(id=brand_id)

        product =Product(
            product_name=product_name,
            category= category_instance,
            brand=brand_instance,
            description=description,
            image1=image1,
            image2=image2,
            image3=image3,
            stock=stock,
            landing_price=landing_price,
            selling_price=selling_price,
            is_listed=is_listed
            )
        product.save()
        return redirect('products')
    return render(request, 'adminn/addproduct.html', {'categories': categories, 'brands': brands})


# function for product list and unlist

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def unlist_produt(request, product_id):
    products = get_object_or_404(Product, pk=product_id)
    if request.method == 'GET':
        if products.is_listed:
            products.is_listed=False
        else:
            products.is_listed=True
        products.save()
        return redirect('products')
    return redirect('products')


# function for update product

@admin_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.all()
    brands = Brand.objects.all()

    if request.method=='POST':
            product_name=request.POST.get('product_name')
            category_id = request.POST.get('category')
            brand_id = request.POST.get('brand')
            description = request.POST.get('description')
            stock = request.POST.get('stock')
            landing_price = request.POST.get('landing_price')
            selling_price = request.POST.get('selling_price')
            is_listed = request.POST.get('is_listed')

            for i in range(1, 4):
                image_field_name = 'image{}'.format(i)
                new_image = request.FILES.get(image_field_name)
                if new_image:
                    setattr(product, image_field_name, new_image)
                    
            category = get_object_or_404(Category, pk=category_id)
            brand = get_object_or_404(Brand, pk=brand_id)
            
            product.product_name=product_name
            product.category = category
            product.brand = brand
            product.description = description
            product.stock = stock
            product.landing_price = landing_price
            product.selling_price = selling_price
            product.is_listed = is_listed

            product.save()
            return redirect('products')
    return render(request,'adminn/editproduct.html',{'product': product,'categories': categories, 'brands': brands})


# function for displaying order details 

def order_details(request):
    orders = Order.objects.all()
    product_names = [", ".join([product.product_name for product in order.products.all()]) for order in orders]
    context = {
        'orders': orders,
        'product_names': product_names
    }
    return render(request, 'adminn/orderdetails.html', context)


# function for updating order status for admin side

def update_order_status(request):
    print('1')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        print('order')
        print(order_id)
        new_status = request.POST.get('new_status')
        print('new status')
        print(new_status)
        
        # Update order status in the database
        try:
            order = Order.objects.get(pk=order_id)
            order.delivery_status = new_status
            order.save()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order does not exist'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# function for display the sales report admin side

def sales_report(request):
    delivered_orders = Order.objects.filter(delivery_status='Delivered')
    product_names = [", ".join([product.product_name for product in order.products.all()]) for order in delivered_orders]
    context = {
        'orders': delivered_orders,
        'product_names': product_names
    }
    return render(request, 'adminn/salesreport.html', context)

