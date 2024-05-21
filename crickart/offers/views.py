from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from adminn.views import admin_required
from .models import Coupon
from django.utils import timezone


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
            return JsonResponse({'success': False, 'message': message})
            
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        total_amount = request.POST.get('total_amount')

        # Validate date fields
        if valid_from and valid_to:
            valid_from_date = timezone.datetime.strptime(valid_from, '%Y-%m-%dT%H:%M')
            valid_to_date = timezone.datetime.strptime(valid_to, '%Y-%m-%dT%H:%M')

            if valid_from_date >= valid_to_date:
                message = "The 'valid from' date must be earlier than the 'valid to' date."
                messages.error(request, message)
                return JsonResponse({'success': False, 'message': message})

        status = 'Active'
        coupon = Coupon(code=code,valid_from=valid_from, valid_to=valid_to, total_amount=total_amount, status=status)
        coupon.save()
        messages.success(request, "Coupon added successfully!")
        return JsonResponse({'success': True, 'message': 'Coupon added successfully!'})
        
    return render(request, 'coupon.html')



# function for edit coupon admin 

def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    
    if request.method == 'POST':
        # Convert "true" string to boolean True, and any other value to False
        active = request.POST.get('active', '').lower() == 'true'
        
        # Update other fields as needed
        code = request.POST.get('code')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        total_amount = request.POST.get('total_amount')
        status = request.POST.get('status')
        
        # Update coupon object with new data
        coupon.code = code
        coupon.valid_from = valid_from
        coupon.valid_to = valid_to
        coupon.active = active
        coupon.total_amount = total_amount
        coupon.status = status
        
        # Save the updated coupon object
        coupon.save()
        return redirect('coupon')     
    return render(request, 'offers/editcoupon.html', {'coupon': coupon})




def unlist_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    if coupon.is_listed:
        coupon.status = 'Expired'
    else:
        coupon.status = 'Active'
    coupon.is_listed = not coupon.is_listed  
    coupon.save()
    return JsonResponse({'message': 'Coupon unlisted successfully.'})


def list_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    if not coupon.is_listed:
        coupon.status = 'Active'
    coupon.is_listed = True
    coupon.save()
    return JsonResponse({'message': 'Coupon listed successfully.'})
