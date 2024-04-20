from . import views 
from django.urls import path

urlpatterns = [

    # urls for admin sign and user management

    path('alogin/',views.adminlogin,name='alogin'),
    path('ahome/',views.ahome,name='ahome'),
    path('alogout/',views.adminlogout,name='alogout'),
    path('userlist/',views.user_list,name='userlist'),
    path('update-status/<int:user_id>/', views.update_status, name='update_status'),

    # urls for categories management 
    
    path('categories/', views.category_list, name='categories'),
    path('categories/add/', views.add_category, name='add_category'), 
    path('categories/edit/<int:category_id>/', views.update_category, name='editcategory'),
    path('categories/unlist/<int:category_id>/', views.unlist_category, name='unlistcategory'),

    # urls for brand management 
 
    path('brand/',views.brand_list,name='brandlist'),
    path('brand/add/', views.add_brand, name='addbrand'),
    path('brand/edit/<int:brand_id>/', views.update_brand, name='updatebrand'),
    path('brand/unlist/<int:brand_id>/', views.unlist_brand, name='unlistbrand'),

    # urls for product management 
    
    path('products/',views.product_list,name='products'),
    path('products/add',views.add_product,name='addproduct'),
    path('products/unlist/<int:product_id>/', views.unlist_produt, name='unlistproduct'),
    path('products/edit/<int:product_id>/', views.update_product, name='updateproduct'),

    # urls for admin order details and order management

    path('orders/',views.order_details,name='orders_view'),



    
    # urls for sales report in admin side 

    path('sales/',views.sales_report,name='sales_report'),   


]
