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
    path('resendotp/',views.resendotp,name='resendotp'), 
   



    # category and shop details
    
    path('category/<str:name>/', views.category_view, name='category_view'),
    path('shop/',views.shop_view,name='shop_view'),
    
    path('filter_products/', views.filter_products, name='filter_products'),
]
