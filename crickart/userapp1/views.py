from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages,auth
from .models import UserProfile
from adminn.models import Category,Product,Brand
from .forms import CreateUserForm
from django.http import JsonResponse
from django.db.models import Q,Min
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
import random 
from django.core.mail import send_mail
from django_otp.plugins.otp_email.models import EmailDevice
from .models import User
import logging
from django.contrib.auth import get_backends
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.urls import reverse



User = get_user_model()

# function for displaying index page to users

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
            lowest_priced_product.selling_price_display = "{:.0f}".format(lowest_price)
            lowest_priced_products[category] = lowest_priced_product

    context = {
        'categories': active_categories,
        'lowest_priced_products': lowest_priced_products
    }
    return render(request, "userapp1/home.html", context)


# function for genereting random otp 

def generate_otp():
    return random.randint(100000, 999999)


# function for user register page 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def userregister(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            # Check if a UserProfile already exists for the user
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            # Update additional fields in the existing UserProfile
            user_profile.phone_number = form.cleaned_data['phone_number']
            user_profile.place = form.cleaned_data['place']
            user_profile.save()

            # Generate OTP and send email
            otp = generate_otp()
            email_device = EmailDevice(user=user, email=user.email, confirmed=False)
            email_device.token = otp
            email_device.save()

            # Print OTP for debugging (remove in production)
            print(otp)

            send_mail(
                'This is CRICKART OTP Code for Registration',
                f'Your OTP code is: {otp}. Do not share it with anyone.',
                'your-email@example.com',
                [user.email],
                fail_silently=False,
            )

            request.session['user_id'] = user.id
            return redirect('verify_otp')
        else:
            # Add form errors to the messages framework
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    context = {'registerform': form}
    return render(request, "userapp1/register.html", context=context)


# function for verify otp 

def verify_otp(request):
    user_id = request.session.get('user_id')
    if not user_id:
        logging.debug("No user_id in session, redirecting to userregister.")
        return redirect('userregister')

    try:
        user = User.objects.get(id=user_id)
        email_device = EmailDevice.objects.get(user=user)
    except User.DoesNotExist:
        logging.error(f"User with id {user_id} does not exist.")
        return redirect('userregister')
    except EmailDevice.DoesNotExist:
        logging.error(f"EmailDevice for user {user_id} does not exist.")
        return redirect('userregister')

    if request.method == 'POST':
        otp = request.POST.get('otp_code')
        logging.debug(f"Received OTP: {otp}")

        if otp == email_device.token:  # Assuming email_device.token stores the OTP
            user.is_active = True
            user.save()
            email_device.confirmed = True
            email_device.save()

            # Find the backend that authenticated the user
            backend_path = None
            for backend in auth.get_backends():
                if backend.get_user(user.id) is not None:
                    backend_path = f'{backend.__module__}.{backend.__class__.__name__}'
                    break

            if backend_path:
                auth.login(request, user, backend=backend_path)  # Log the user in with the specified backend
                messages.success(request, f'OTP sent to {user.email}. Enter OTP to log in.')
                logging.debug(f"OTP verified successfully for user {user.email}. Redirecting to login page.")
                return redirect('userlogin')  # Redirect to login page after successful activation
            else:
                logging.error("No suitable authentication backend found for the user.")
                messages.error(request, 'Authentication error. Please try again.')
        else:
            messages.error(request, 'Invalid OTP')
            logging.debug("Invalid OTP entered.")

    return render(request, 'userapp1/verify_otp.html')
    
# function for resend otp 

def resend_otp(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('userregister')  # Redirect to registration if no user_id in session

    user = User.objects.get(id=user_id)
    email_device = EmailDevice.objects.get(user=user)
    otp = generate_otp()
    email_device.token = otp
    email_device.save()

    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp}',
        'your-email@example.com',
        [user.email],
        fail_silently=False,
    )

    messages.success(request, 'A new OTP has been sent to your email.')
    return redirect('verify_otp')


# function for forget password 

@csrf_protect
def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                otp = generate_otp()
                request.session['reset_otp'] = otp
                request.session['email'] = email

                logger.debug(f"Generated OTP: {otp}")

                subject = "This is a password reset mail"
                message = f'Your OTP for resetting your password is {otp}.'
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                
                return render(request, 'userapp1/newpassword.html')
        return render(request, 'userapp1/forget_password.html', {'error': 'Email not found'})
    return render(request, 'userapp1/forget_password.html')
    
# function for forget otp verify

logger = logging.getLogger(__name__)

# Helper function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

@csrf_protect
def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                otp = generate_otp()
                request.session['reset_otp'] = otp
                request.session['email'] = email

                logger.debug(f"Generated OTP: {otp}")
                print(f"Generated OTP: {otp}")

                subject = "This is a password reset mail"
                message = f'Your OTP for resetting your password is {otp}.'
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                
                return render(request, 'userapp1/newpassword.html')
        return render(request, 'userapp1/forget_password.html', {'error': 'Email not found'})
    return render(request, 'userapp1/forget_password.html')



# this function is used to check the password is matching or not
@csrf_protect
def otp_verify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        session_otp = request.session.get('reset_otp')
        email = request.session.get('email')

        if otp == session_otp:
            if new_password == confirm_password:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                # Clear the session
                request.session.flush()
                return render(request, 'userapp1/newpassword.html', {'success': 'Password updated successfully'})
            else:
                return render(request, 'userapp1/newpassword.html', {'error': 'Passwords do not match'})
        else:
            return render(request, 'userapp1/newpassword.html', {'error': 'Invalid OTP'})

    return render(request, 'userapp1/newpassword.html')




# function for forget password 
def rest_password(request):
    return render(request,'userapp1/newpassword.html')


# function for user login page 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def user_login(request): 
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


# function for  user log_out page 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)  
@never_cache
@login_required(login_url='userlogin')
def userlogout(request):
    logout(request)
    request.session.flush()
    response = redirect('home')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


# function for product deyails 


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    similar_products = Product.objects.filter(category=product.category).exclude(pk=product_id)[:5]
    
    # Calculate the discounted price for the current product
    discounted_price = product.get_discounted_price()
    
    context = {
        'product': product,
        'discounted_price': discounted_price,
        'similar_products': similar_products
    }
    
    return render(request, 'userapp1/productdetails.html', context)



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


# function  for shop view filter and category wise

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def shop_view(request):
    products = Product.objects.filter(
        category__is_listed=True,
        brand__is_listed=True,
        is_listed=True
    )
    
    serialized_products = [{
        'product_name': product.product_name,
        'selling_price': product.selling_price,
        'discounted_price': product.get_discounted_price(),  # Include discounted price
        'image_url': product.image1.url if product.image1 else '',  # Use image2 URL if available
        'id': product.id
    } for product in products]
    
    return render(request,'userapp1/shop.html',{'products':serialized_products})




# function for filtering the products from shoppage

from operator import attrgetter

def filter_products(request):
    sort_name = request.GET.get('sortName')
    sort_price = request.GET.get('sortPrice')
    category_id = request.GET.get('category')

    filtered_products = Product.objects.filter(
        category__is_listed=True,
        brand__is_listed=True,
        is_listed=True
    )

    # Calculate the discounted price for each product
    for product in filtered_products:
        product.discounted_price = product.get_discounted_price()

    if sort_name == 'AZ':
        filtered_products = sorted(filtered_products, key=attrgetter('product_name'))
    elif sort_name == 'ZA':
        filtered_products = sorted(filtered_products, key=attrgetter('product_name'), reverse=True)

    if sort_price == '1':
        filtered_products = [product for product in filtered_products if 100 <= product.discounted_price <= 500]
    elif sort_price == '2':
        filtered_products = [product for product in filtered_products if 500 <= product.discounted_price <= 1000]
    elif sort_price == '3':
        filtered_products = [product for product in filtered_products if 1000 <= product.discounted_price <= 1500]
    elif sort_price == '4':
        filtered_products = [product for product in filtered_products if product.discounted_price >= 1500]

    if category_id:
        filtered_products = [product for product in filtered_products if product.category_id == int(category_id)]

    serialized_products = [{
        'product_name': product.product_name,
        'discounted_price': product.discounted_price,
        'selling_price': product.selling_price,
        'image_url': product.image2.url if product.image2 else '', # Use image1 URL if available
        'id': product.id
    } for product in filtered_products]

    return render(request, 'userapp1/shop.html', {
        'products': serialized_products,
        'categories': Category.objects.all()# Pass all categories to the template
    })



# function for searching the products from shoppage

def search_products(request):
    query = request.GET.get('query')

    if query:
        # Filter products by product name, category name, or description
        filtered_products = Product.objects.filter(
            Q(product_name__icontains=query) | 
            Q(category__name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        filtered_products = Product.objects.order_by('product_name')

    serialized_products = [{
        'product_name': product.product_name,
        'selling_price': product.selling_price,
        'discounted_price': product.get_discounted_price(),  # Calculate discounted price
        'image_url': product.image3.url if product.image3 else '',  # Use image3 URL if available
        'id': product.id
    } for product in filtered_products]

    return render(request, 'userapp1/shop.html', {
        'products': serialized_products,
        'categories': Category.objects.all()
    })
