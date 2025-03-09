from django.shortcuts import render, redirect
from .models import Task
from datetime import datetime, date

# Create your views here.
def task_list(request):
    search_query = request.GET.get("q", "")
    tasks = Task.objects.all()

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    return render(request, "task_list.html", {"tasks": tasks, "search_query": search_query})

def task_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date_str = request.POST.get("due_date")  

        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

        today = date.today()
        if due_date < today:
            status = "Overdue"
        elif due_date == today:
            status = "Due Today"
        else:
            status = "Upcoming"

        Task.objects.create(title=title, description=description, due_date=due_date, status=status)

        return redirect("task_list")

    return render(request, "task_form.html")


def task_update(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return redirect("task_list")  

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        due_date_str = request.POST.get("due_date")

        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        task.due_date = due_date  

        today = date.today()
        if due_date < today:
            task.status = "Overdue"
        elif due_date == today:
            task.status = "Due Today"
        else:
            task.status = "Upcoming"

        task.save()
        return redirect("task_list")

    return render(request, "task_form.html", {"task": task})


def task_delete(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return redirect("task_list") 

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "task_confirm_delete.html", {"task": task})