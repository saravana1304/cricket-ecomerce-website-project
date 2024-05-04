from django.urls import path
from . import views 


urlpatterns = [

    # urls for user profle based functions 

    path('offer/', views.offer, name='offer'), 
]