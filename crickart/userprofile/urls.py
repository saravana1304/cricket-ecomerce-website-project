from django.urls import path
from . import views 


urlpatterns = [
   
    path('profile/',views.userprofile,name='profile'), 
    path('cartview/',views.cart_view,name='cartview'),
]