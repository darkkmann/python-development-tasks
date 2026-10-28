from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task-list"), path("register/", views.register, name="register"),
    path("tasks/create/", views.create_task, name="task-create"), path("tasks/<int:task_id>/toggle/", views.toggle_task, name="task-toggle"),
    path("tasks/<int:task_id>/delete/", views.delete_task, name="task-delete"),
]
