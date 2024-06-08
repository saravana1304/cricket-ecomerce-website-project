from django.urls import path
from . import views 


urlpatterns = [
    # home page and user login logout

    path('',views.userindex,name='home'),  
    path('userregister/',views.userregister,name='userregister'),
    path('user_login/', views.user_login, name='userlogin'), 
    path('logout/',views.userlogout,name='logout'),
   

    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resendotp'), 
    path('forget_pasword/', views.forget_password, name='forgetpass'),
    path('reset_pasword/', views.rest_password, name='resetpass'),
    path('otp_verify/', views.otp_verify, name='otp_verify'),


    # product details

    path('productdetails/<int:product_id>/',views. product_details,name='productdetails'),

    # category and shop details
    
    path('category/<str:name>/', views.category_view, name='category_view'),
    path('shop/',views.shop_view,name='shop_view'),
    
    path('filter_products/', views.filter_products, name='filter_products'),
    path('search/', views.search_products, name='search_products'),
]
