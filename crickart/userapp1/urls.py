
from django.urls import path
from . import views 


urlpatterns = [
    path('',views.userindex,name='home'),  
    path('userregister/',views.userregister,name='userregister'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('contactus/',views.contactus,name='contactus'),
    path('logout/',views.userlogout,name='logout'),
   
   
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),
    path('otp/',views.otp,name='otp'),
    

   
]
