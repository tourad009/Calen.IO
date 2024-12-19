from django.urls import path
from . import views

urlpatterns = [
    # Création d'une tâche
    path('tasks/create/', views.create_task, name='create_task'),
    # Mise à jour d'une tâche
    path('tasks/update/<int:task_id>/', views.update_task, name='update_task'),
    # Suppression d'une tâche
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    # Liste des tâches
    path('tasks/', views.task_list, name='task_list'),
]
