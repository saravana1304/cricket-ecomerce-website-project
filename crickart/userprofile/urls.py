from django.urls import path
from . import views 


urlpatterns = [
   
    path('profile/',views.userprofile,name='profile'), 
    path('cartview/',views.cart_view,name='cartview'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]