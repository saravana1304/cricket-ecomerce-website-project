from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from adminn.views import admin_required
from .models import Coupon

# Create your views here.

@admin_required
def coupon_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'offers/coupon.html', {'coupons': coupons})

@admin_required
def add_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        
        # Check if a coupon with the same code already exists
        if Coupon.objects.filter(code=code).exists():
            message = f"A coupon with code '{code}' already exists."
            messages.error(request, message)
            return JsonResponse({'success': False, 'message': message})  # Return JSON response with error message
            
        discount = request.POST.get('discount')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        total_amount = request.POST.get('total_amount')
        status = 'Active'
        coupon = Coupon(code=code, discount=discount, valid_from=valid_from, valid_to=valid_to, total_amount=total_amount, status=status)
        coupon.save()
        messages.success(request, "Coupon added successfully!")
        return JsonResponse({'success': True, 'message': 'Coupon added successfully!'})  # Return JSON response with success message
        
    return render(request, 'coupon.html')




@admin_required
def editcoupon(request):
    return render(request,'offers/editcoupon.html')


@admin_required
def removecoupon(request):
    return render(request,'offers/deletecoupon.html')