from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from userapp1.models import UserProfile
from userprofile.models import Address
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from .models import Cart 
from adminn.models import Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import AddressForm



# Create your views here.

# code for viewing user profile 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)  
@never_cache
@login_required(login_url='userlogin')
def userprofile(request):
    if not  request.user.is_authenticated:
        return redirect('home')
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        addresses = Address.objects.filter(user_profile=user_profile)
        request.session['user_profile_id'] = user_profile.id
        return render(request,'userprofile/profile.html',{'user_profile': user_profile,'addresses':addresses})

# code for add address
@login_required(login_url='userlogin')
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_profile_id = request.session.get('user_profile_id')
            address.save()
            return JsonResponse({'success': True, 'message': 'Address added successfully'}, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)
    else:
        form = AddressForm()
    return render(request, 'userprofile/addaddress.html', {'form': form})


# code for cart_view

@cache_control(no_cache=True,must_revalidate=True,no_store=True) 
@never_cache
def cart_view(request):
    if request.user.is_authenticated:  
        cart_items = Cart.objects.filter(user=request.user)
        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.total_price() for item in cart_items) 
        return render(request, 'userprofile/usercart.html', {'cart_items': cart_items,'total_quantity': total_quantity, 'total_price': total_price})
    else:
        return redirect('userlogin')

# code for add_to_cart 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)  
@never_cache
def add_to_cart(request, product_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:  
            return redirect('userlogin') 
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            selling_price=product.selling_price 
        )
        
        if created:
            cart_item.quantity = 0

        if quantity <= product.stock:  
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('cartview')
    

# delete from the cart 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)  
@never_cache
def delete_item_from_cart(request, item_id):
    try:
        cart_item = Cart.objects.get(id=item_id, user=request.user)
        cart_item.delete() 
        return JsonResponse({'message': 'Item deleted successfully'})
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

# clear cart for delete all items 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)  
@never_cache
def clear_cart(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        cart_items.delete()
        response_data = {'success': True, 'message': 'Your cart has been cleared successfully.'}
        return JsonResponse(response_data)
    else:
        response_data = {'success': False, 'error': 'Invalid request method.'}
        return JsonResponse(response_data, status=400)  


# check_outpage  

@login_required(login_url='userlogin')
def checkout_page(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    return render(request, 'userprofile/checkout.html', {'user_profile': user_profile})
          