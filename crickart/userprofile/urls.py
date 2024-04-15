from django.urls import path
from . import views 


urlpatterns = [

    # urls for user profle based functions 

    path('profile/', views.userprofile, name='profile'), 
    path('add_address/', views.add_address, name='addaddress'),
    path('update_address/<int:address_id>/', views.update_address, name='updateaddress'),
    path('delete_address/<int:address_id>/', views.delete_address, name='deleteaddress'),
    
    # urls for displaying user orders 

    path('user_order/', views.user_order, name='user_order'), 

    # urls for user cart based functions

    path('cartview/',views.cart_view,name='cartview'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/<int:item_id>/delete/', views.delete_item_from_cart, name='delete_item_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('update-cart-item-quantity/<int:item_id>/<int:quantity>/', views.update_cart_item_quantity, name='update_cart_item_quantity'),
    
    # urls for checkout and place_order functions

    path('checkout/', views.checkout_page, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),

]