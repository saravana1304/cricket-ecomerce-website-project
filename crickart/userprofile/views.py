from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from userapp1.models import UserProfile
from django.views.decorators.cache import never_cache
from .models import Cart
from adminn.models import Product

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
    if request.user.is_authenticated:  
        cart_items = Cart.objects.filter(user=request.user)
        return render(request, 'userprofile/usercart.html', {'cart_items': cart_items})
    else:
        return redirect('userlogin')



def add_to_cart(request, product_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:  # Check if the user is authenticated
            return redirect('userlogin') 
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            selling_price=product.selling_price 
        )
        
        if created:
            cart_item.quantity = 1

        if quantity <= product.stock:  
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('cartview')