from django.urls import path
from . import views 


urlpatterns = [
    # home page and user login logout

    path('',views.userindex,name='home'),  
    path('userregister/',views.userregister,name='userregister'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('contactus/',views.contactus,name='contactus'),
    path('logout/',views.userlogout,name='logout'),
   

    path('otp/',views.otp,name='otp'),
    path('resendotp/',views.resendotp,name='resendotp'),  

    # product details

    path('productdetails/<int:product_id>/',views.product_deatils,name='productdetails'),
]
