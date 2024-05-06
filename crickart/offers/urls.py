from django.urls import path
from . import views 


urlpatterns = [

    # urls for user profle based functions 

    path('coupon/', views.coupon_list, name='coupon'), 
    path('addcoupon/', views.add_coupon, name='addcoupon'),
]