from . import views 
from django.urls import path

urlpatterns = [
    path('alogin/',views.adminlogin,name='alogin'),
    path('ahome/',views.ahome,name='ahome'),
    path('alogout/',views.adminlogout,name='alogout'),

    path('userlist/',views.userlist,name='userlist'),
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
]