from django.urls import path
from . import views 


urlpatterns = [
    # home page and user login logout

    path('',views.userindex,name='home'),  
    path('userregister/',views.userregister,name='userregister'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('logout/',views.userlogout,name='logout'),
   

    path('userregister/', views.userregister, name='userregister'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resendotp'), 

    # product details

    path('productdetails/<int:product_id>/',views. product_details,name='productdetails'),

   

    # category and shop details
    
    path('category/<str:name>/', views.category_view, name='category_view'),
    path('shop/',views.shop_view,name='shop_view'),
    
    path('filter_products/', views.filter_products, name='filter_products'),
    path('search/', views.search_products, name='search_products'),
]
