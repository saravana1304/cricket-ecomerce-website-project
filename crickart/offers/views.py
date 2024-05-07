from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from adminn.views import admin_required
from .models import Coupon

# Create your views here.

#this function is used for displaying the all details to user  
@admin_required
def coupon_list(request):
    coupons = Coupon.objects.all().order_by('-id')
    return render(request, 'offers/coupon.html', {'coupons': coupons})


# this function is used for adding new coupon for our database
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




def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    
    if request.method == 'POST':
        # Convert "true" string to boolean True, and any other value to False
        active = request.POST.get('active', '').lower() == 'true'
        
        # Update other fields as needed
        code = request.POST.get('code')
        discount = request.POST.get('discount')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        total_amount = request.POST.get('total_amount')
        status = request.POST.get('status')
        
        # Update coupon object with new data
        coupon.code = code
        coupon.discount = discount
        coupon.valid_from = valid_from
        coupon.valid_to = valid_to
        coupon.active = active
        coupon.total_amount = total_amount
        coupon.status = status
        
        # Save the updated coupon object
        coupon.save()
        return redirect('coupon')     
    return render(request, 'offers/editcoupon.html', {'coupon': coupon})




def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    coupon.delete()
    return JsonResponse({'message': 'Coupon deleted successfully.'})
