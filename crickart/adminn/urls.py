from . import views 
from django.urls import path

urlpatterns = [
    path('alogin/',views.home,name='adminlogin'),
    path('ahome/',views.home,name='adminnhome'),
]