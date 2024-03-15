from . import views 
from django.urls import path

urlpatterns = [
    path('alogin/',views.adminlogin,name='alogin'),
    path('ahome/',views.ahome,name='ahome'),
    path('alogout/',views.adminlogout,name='alogout'),
    path('userlist/',views.user_list,name='userlist'),
    path('update-status/<int:user_id>/', views.update_status, name='update_status'),

    path('categories/', views.category_list, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),  
]