from django.urls import path
from .views import *

urlpatterns=[
    path("",login_,name="login_"),
    path("register/",register,name="register"),
    path("profile/",profile,name="profile"),
    path("update/",update,name="update"),
    path("reset_pass/",reset_pass,name="reset_pass"),
    path("forgetpass",forgetpass,name="forgetpass"),
    path("newpass/",newpass,name="newpass"),
    path("logout/",logout_,name="logout_"),
   

]