from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    model=Products
    list_display=["id","pname","pcategory","pimage"]


admin.site.register(Products,ProductAdmin)
