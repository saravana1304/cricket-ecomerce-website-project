from django.urls import path
from . import views 


urlpatterns = [

    # urls for user profle based functions 

    path('coupon/', views.coupon_list, name='coupon'), 
    path('addcoupon/', views.add_coupon, name='addcoupon'),
    path('coupons/edit/<int:coupon_id>/', views.edit_coupon, name='editcoupon'),
    path('coupons/delete/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),   
]