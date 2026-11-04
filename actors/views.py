from django.shortcuts import render,redirect
from django.http import HttpResponse
from actors.forms import ActorForm
# Create your views here.


def addActor(request):
    if request.method=="POST":
        form=ActorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            return HttpResponse("Invalid data")
    else:
        form=ActorForm()
    return render(request,"add-actors.html",{"my_form":form})