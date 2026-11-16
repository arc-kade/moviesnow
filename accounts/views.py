from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Profile

# Create your views here.

def signUp(request):
    if request.method =="POST":
        email = request.POST['email']
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        password = request.POST['password']
        if User.objects.filter(username=email).exists():  #checks whether the value stored in email exists in the username field
            return redirect("login")
        else:
            with transaction.atomic():
                user = User.objects.create_user(username=email,first_name=f_name,last_name=l_name,password=password)
                Profile.objects.create(
                    user=user,
                    place=request.POST["place"],
                    profile_pic=request.FILES["profile_pic"],
                    dob=request.POST["dob"],
                )
            return redirect("login")
    return render(request,"register.html")


def signIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            return HttpResponse("Invalid username or password")

    return render(request,"login.html")

@login_required(login_url="login")
def Logout(request):
    auth.logout(request)
    return redirect("/")

        
    return render(request,"login.html")
