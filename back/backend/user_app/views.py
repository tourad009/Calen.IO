from django.shortcuts import  redirect
from django.contrib.auth import authenticate, login

from django.contrib import messages
from .models import User
from django.http import JsonResponse
import json
from django.views.decorators.csrf import  ensure_csrf_cookie

from django.middleware.csrf import get_token
from django.http import JsonResponse

@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'message': 'CSRF cookie set'})

@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            username = body.get('username')
            password = body.get('password')
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)

            user = User.objects.create_user(username=username, password=password)
            user.save()

            return JsonResponse({'message': 'User created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)  # Traiter la requête en tant que JSON
            username = body.get('username')
            password = body.get('password')

            if username and password:
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return JsonResponse({'message': 'You are now logged in.'}, status=200)
                else:
                    return JsonResponse({'error': 'Invalid username or password.'}, status=400)
            else:
                return JsonResponse({'error': 'Please provide both username and password.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)