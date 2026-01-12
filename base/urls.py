from django.urls import path
from .views import *

urlpatterns=[
    path("",home,name="home"),
    path("addtocart/<int:pk>",addtocart,name="addtocart"),
    path("cart/",cart,name="cart"),
    path("remove/<int:pk>",remove,name="remove"),
    path("decrease/<int:pk>",decrease,name="decrease"),
    path("increase/<int:pk>",increase,name="increase"),

    
    
]