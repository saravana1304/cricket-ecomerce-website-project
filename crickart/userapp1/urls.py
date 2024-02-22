
from django.urls import path
from . import views 


urlpatterns = [
    path('',views.userindex,name='home'),  
    path('userregister/',views.userregister,name='register'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('contactus/',views.contactus,name='contactus'),
]
