from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render

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
            user = User.objects.create_user(username=email,first_name=f_name,last_name=l_name,password=password)    #creates a new user instance to the database
            user.save()
            return redirect("login")
    return render(request,"register.html")


def signIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
    return render(request,"login.html")
