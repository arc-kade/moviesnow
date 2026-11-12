from django.shortcuts import render,redirect
from django.http import HttpResponse
from actors.forms import ActorForm
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .models import Actors
from django.urls import reverse_lazy
# Create your views here.


# def addActor(request):
#     if request.method=="POST":
#         form=ActorForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("/")
#         else:
#             return HttpResponse("Invalid data")
#     else:
#         form=ActorForm()
#     return render(request,"add-actors.html",{"my_form":form})

class AddActor(CreateView):
    model=Actors
    form_class=ActorForm
    template_name="add-actors.html"
    success_url=reverse_lazy("actors_list")

class AllActors(ListView):
    model=Actors
    template_name="actors-list.html"
    context_object_name="actors"

