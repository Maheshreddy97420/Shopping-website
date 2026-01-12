from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        cartproduct_count = CartModel.objects.filter(host=request.user).count()
    else:
        cartproduct_count= False

    #search operation if there are no records present
    nomatch = False
    trend =False
    offer = False

    #Search Bar
    if 'q' in request.GET:
        d=request.GET['q']
        all_products=Products.objects.filter(Q(Q(pname__icontains=d) | Q(pdesc__icontains=d)))
        print(len(all_products))
        if len(all_products) == 0:
            nomatch =True


    #Category 
    elif "cat" in request.GET:
        cat=request.GET['cat']
        all_products=Products.objects.filter(pcategory=cat)


    # Trending Product
    elif "trending" in request.GET:
        all_products=Products.objects.filter(trending=True)
        trend =True

    #Offer Product
    elif "offer" in request.GET:
        all_products=Products.objects.filter(offer=True)
        offer =True

    else:
        # To Display All products
        all_products =Products.objects.all()

    category=[]
    for i in Products.objects.all():
        if i.pcategory not in category:
            category +=[i.pcategory]
    
    return render(request,"home.html",{"all_products":all_products,"nomatch":nomatch,"category":category ,"cartproduct_count":cartproduct_count,"trend":trend,"offer":offer})

@login_required(login_url='login_')
def addtocart(request,pk):
    product =Products.objects.get(id=pk)
    try:
        cp = CartModel.objects.get(pname=product.pname,host=request.user)
        cp.quantity+=1
        cp.totalPrice+=product.price
        cp.save()
        return redirect('home')


    except:
        CartModel.objects.create(
            pname =product.pname,
            price=product.price,
            pcategory =product.pcategory,
            quantity = 1,
            totalPrice =product.price,
            pimage=product.pimage,
            host =request.user

        )
        return redirect('home')
    return redirect('home')


@login_required(login_url='login_')
def cart(request):
    cartproduct_count=CartModel.objects.filter(host=request.user).count()

    data=CartModel.objects.filter(host=request.user)
    TA = 0
    for i in data:
        # print(i.totalPrice)
        TA +=i.totalPrice
    return render(request,'cart.html',{"data":data , "TA":TA,"profile_nav":True,"cartproduct_count":cartproduct_count})

@login_required(login_url='login_')
def remove(request,pk):
    cartproducts=CartModel.objects.get(id=pk)
    cartproducts.delete()
    return redirect('cart')


def increase(request,pk):
    cp = CartModel.objects.get(id=pk,host=request.user)
    cp.quantity+=1
    cp.totalPrice+=cp.price
    cp.save()
    return redirect('cart')


def decrease(request,pk):
    cp = CartModel.objects.get(id=pk,host=request.user)
    if cp.quantity >1:
        cp.quantity-=1
        cp.totalPrice-=cp.price
        cp.save()
    else :
        cp.delete()
        return redirect('cart')
    return redirect('cart')

def knowus(request):
    return render(request,'knowus.html',{"profile_nav":True})

def support(request):
    return render(request,'support.html',{"profile_nav":True})

def proceed(request):
    return render(request,'proceed.html')

def details(request,pk):
    a=Products.objects.get(id=pk)
    return render(request,'details.html',{"a":a})