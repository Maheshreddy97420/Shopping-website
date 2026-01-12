from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from base.models import CartModel



# Create your views here.
def login_(request):

    if request.method =="POST":
        username = request.POST['username']
        password= request.POST['password']
        u = authenticate(username=username,password=password)
        if u:
            login(request,u)
            return redirect('home')
        else :
            return render(request,"login_.html",{"status":"Incorrect Username or Password"})

    return render(request,"login_.html",{"login_nav":True})

def logout_(request):
    logout(request)
    return redirect("login_")

def register(request):
    if request.method =="POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password= request.POST['password']
        try:
            a=User.objects.get(username=username)
            return render(request,"register.html",{"status":"Username Already Exits Try New Username"})

        except:
            a=User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username
            )
            a.set_password(password)
            a.save()
            return redirect('login_')
    return render(request,"register.html",{"login_nav":True})


@login_required(login_url='login_')
def profile(request):
    cartproduct_count = CartModel.objects.filter(host=request.user).count()
    return render(request,"profile.html",{"profile_nav":True,"cartproduct_count":cartproduct_count})

login_required(login_url='login_')
def update(request):
    cartproduct_count = CartModel.objects.filter(host=request.user).count()
    d=request.user
    if request.method =="POST":
        
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        d.username=username
        d.first_name=first_name
        d.last_name=last_name
        d.email=email
        d.save()
        return redirect('profile')
    return render(request,"update.html",{"profile_nav":True,"cartproduct_count":cartproduct_count})

login_required(login_url='login_')
def reset_pass(request):
    cartproduct_count = CartModel.objects.filter(host=request.user).count()
    opass =request.user
    if request.method == "POST":
        if "oldpass" in request.POST:
            old = request.POST.get('oldpass')
            new = request.POST.get('newpass')
            renew = request.POST.get('renewpass')

            if not opass.check_password(old):
                return render(request,"reset_pass.html",{"status":"Incorrect Old Password"})
            if new != renew:
                return render(request,"reset_pass.html",{"status":"The new password is not matching the re-enter Password"})
            opass.set_password(new)
            opass.save()
            return redirect('login_')
    return render(request,"reset_pass.html",{"profile_nav":True,"cartproduct_count":cartproduct_count})

def forgetpass(request):
    
    if request.method == "POST":
        cusername=request.POST.get('username')
        try:
            user= User.objects.get(username=cusername)

            request.session['user_fp']=user.username
            return redirect('newpass')
        except User.DoesNotExist:
            return render(request,'forgetpass.html',{"error":True})

    return render(request,"forgetpass.html",{"login_nav":True})

def newpass(request):
    v_username=request.session.get('user_fp')
    if v_username is None:
        return redirect('forgetpass')
    v_user=User.objects.get(username=v_username)
    if request.method =="POST":
        new_pass =request.POST.get('password')
        if v_user.check_password(new_pass):
            return render(request,"newpass.html",{"error":"New password should not similar to the old passwords"})
        v_user.set_password(new_pass)
        v_user.save()

        del request.session['user_fp']
        return redirect('login_')
    return render(request,"newpass.html",{"login_nav":True})