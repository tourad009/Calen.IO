from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
import json
from .models import Task
from .forms import TaskForm


@login_required
def task_list(request):
    """
    Vue pour obtenir la liste des tâches de l'utilisateur connecté.
    """
    tasks = Task.objects.filter(user=request.user).order_by('-due_date')
    tasks_data = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'end_date': task.end_date.isoformat() if task.end_date else None,
        'completed': task.completed,
        'priority': task.priority,
    } for task in tasks]
    
    print("Tâches envoyées:", tasks_data)  # Debug
    return JsonResponse(tasks_data, safe=False)


@login_required
@csrf_exempt
def create_task(request):
    """
    Vue pour créer une nouvelle tâche.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        form = TaskForm(data)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return JsonResponse({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date,
                'end_date': task.end_date,
                'completed': task.completed,
                'priority': task.priority,
            }, status=201)
        return JsonResponse({'errors': form.errors}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@login_required
@csrf_exempt
def update_task(request, task_id):
    """
    Vue pour mettre à jour une tâche existante.
    """
    if request.method != 'PUT':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    task = get_object_or_404(Task, id=task_id)
    if task.user != request.user:
        raise PermissionDenied()
    
    try:
        data = json.loads(request.body)
        form = TaskForm(data, instance=task)
        if form.is_valid():
            task = form.save()
            return JsonResponse({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date,
                'end_date': task.end_date,
                'completed': task.completed,
                'priority': task.priority,
            })
        return JsonResponse({'errors': form.errors}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@login_required
@csrf_exempt
def delete_task(request, task_id):
    """
    Vue pour supprimer une tâche.
    """
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    task = get_object_or_404(Task, id=task_id)
    if task.user != request.user:
        raise PermissionDenied()
    
    task.delete()
    return JsonResponse({'message': 'Task deleted successfully'})


@login_required
def task_detail(request, task_id):
    """
    Vue pour obtenir les détails d'une tâche spécifique.
    """
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    task_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date,
        'end_date': task.end_date,
        'completed': task.completed,
        'priority': task.priority,
    }
    return JsonResponse(task_data)
