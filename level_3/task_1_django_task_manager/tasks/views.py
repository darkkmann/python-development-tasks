from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistrationForm, TaskForm
from .models import Task


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task-list")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def task_list(request):
    return render(request, "tasks/list.html", {"tasks": Task.objects.filter(owner=request.user), "form": TaskForm()})


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
    return redirect("task-list")


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.owner != request.user and not request.user.is_staff:
        raise Http404
    if request.method == "POST":
        task.completed = not task.completed
        task.save(update_fields=["completed"])
    return redirect("task-list")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.owner != request.user and not request.user.is_staff:
        raise Http404
    if request.method == "POST":
        task.delete()
    return redirect("task-list")
