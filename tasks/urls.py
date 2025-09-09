from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_task, name="task-create"),
    path("toggle/<int:pk>/", views.toggle_task, name="task-toggle"),
    path("update/<int:pk>/", views.update_task, name="task-update"),
    path("delete/<int:pk>/", views.delete_task, name="task-delete"),
    path("search/", views.search_tasks, name="task-search"),
    path("detail/<int:pk>/", views.task_detail, name="task-detail"),
]
