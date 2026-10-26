from django.http import HttpResponse #custom import
from django.shortcuts import render,redirect #to return HTML files
from todoapp.models import ToDos


# Create your views here.
def Home(request): #user defined function
    if request.method=="POST":
        task_data=request.POST['task_name'] #saves data from task_name in the from from index.html
        ToDos(task=task_data).save() #inserts the data into todo
    is_authenticated = True
    myTasks = ToDos.objects.all() #SELECT* FROM in SQL
    print(myTasks)

    context={"task":myTasks,"status":is_authenticated}
    return render(request,"index.html",{"tasks": myTasks}) #calls /templates/index.html

def editTask(request,task_id):
    task_detail=ToDos.objects.get(id=task_id) #column
    if request.method=="POST":
        task_data=request.POST['task_name'] #value
        status = request.POST.get('status',False)
        if status:
            task_detail.is_completed=status.capitalize()

        else:
            task_detail.is_completed=status

        task_detail.task=task_data #object.column= value
        task_detail.save()
        return redirect("/")
    return render(request,"edit-task.html",{"my_task":task_detail})

def deleteTask(request,task_id):
    task = ToDos.objects.get(id=task_id)
    task.delete() #built-in function
    return redirect("/")

def TestResponse(request):
    return HttpResponse("Hello world")

def About(request):
    return render(request,"about.html")

def Contact(request):
    return render(request,"contact.html")
