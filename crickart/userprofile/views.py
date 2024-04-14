from django.shortcuts import render,redirect
from django.shortcuts import render, redirect, get_object_or_404
from userapp1.models import UserProfile
from userprofile.models import Address,Order
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from .models import Cart 
from adminn.models import Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import AddressForm
from django.db.models import F
from django.db import transaction
from datetime import datetime, timedelta,timezone


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


# code for updating address
@login_required(login_url='userlogin')
def update_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
   
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Address updated successfully'}, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'userprofile/editaddress.html', {'form': form})


# code for delete address for user
def delete_address(request, address_id):
    try:
        address = get_object_or_404(Address, id=address_id)
        address.delete()
        return JsonResponse({'success': True})
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Address does not exist'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


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
@never_cache
def add_to_cart(request, product_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('userlogin')

        product = get_object_or_404(Product, pk=product_id)
        max_quantity = product.stock  # Maximum quantity available for the product

        requested_quantity = int(request.POST.get('quantity', 1))

        if requested_quantity > max_quantity:
            requested_quantity = max_quantity  # Limit the quantity to the maximum available

        # Check if the item already exists in the cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            selling_price=product.selling_price
        )

        if not created:  # Item already exists in the cart
            cart_item.quantity += requested_quantity  # Increase the quantity
            if cart_item.quantity > max_quantity:
                cart_item.quantity = max_quantity  # Limit the quantity to the maximum available
            cart_item.save()
        else:
            cart_item.quantity = requested_quantity
            cart_item.save()

        return redirect('cartview')
    

# code for increase qty 

def update_cart_item_quantity(request, item_id, quantity):
    try:
        cart_item = Cart.objects.get(id=item_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({'success': True, 'message': 'Cart item quantity updated successfully'})
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}) 
    

# code for  delete from the cart 

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

@login_required
def checkout_page(request):
    user = request.user
    user_profile_address = UserProfile.objects.filter(user=user).first()
    shipping_addresses = Address.objects.filter(user_profile=user_profile_address)

    if request.method == 'POST' and 'product_id' in request.POST:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = Product.objects.get(pk=product_id)

        existing_item = Cart.objects.filter(user=user, product=product).first()

        if existing_item:
            existing_item.quantity = F('quantity') + quantity
            existing_item.save()
        else:
            new_item = Cart(user=user, product=product, quantity=quantity, selling_price=product.selling_price)
            new_item.save()

        return redirect('checkout_page')

    usercart = Cart.objects.filter(user=user)
    
    total_price_list = []
    for item in usercart:
        total_price_list.append(item.quantity * item.selling_price)
    total_price = sum(total_price_list)

    # Calculate total price for each item
    for cart_item in usercart:
        cart_item.total_price = cart_item.quantity * cart_item.selling_price

    context = {
        'user': user,
        'userprofile_address': user_profile_address,
        'cart_items': usercart,
        'shipping_addresses': shipping_addresses,
        'total_price': total_price,
    }

    return render(request, 'userprofile/checkout.html', context)


# function for place order
@transaction.atomic
def place_order(request):
    try:
        user = request.user
        user_profile_address = UserProfile.objects.get(user=user)
        payment_method = request.POST.get('payment_method')
        address_method = request.POST.get('address_method')

        if not user_profile_address:
            raise ValueError("User profile address not found.")

        if not payment_method:
            raise ValueError("Payment method is required.")

        if not address_method:
            raise ValueError("Address method is required.")

        # Fetch the products from the cart and extract their IDs
        cart_items = Cart.objects.filter(user=user)
        product_ids = [item.product_id for item in cart_items]

        # Create the order
        with transaction.atomic():
            order = Order.objects.create(
                user_profile=user_profile_address,
                total_qty=sum(item.quantity for item in cart_items),
                total_price=sum(item.total_price() for item in cart_items),
                address=address_method,
                payment=payment_method,
                delivery_status='Pending',
                order_date=timezone.now(),
            )

            # Associate products with the order
            order.product_set.set(product_ids)

            # Clear the user's cart
            cart_items.delete()

        return JsonResponse({'success': True, 'message': 'Your order has been placed successfully!'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)



@login_required
def user_order(request):
    return render(request,'userprofile/userorder.html')
