from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import User
import json


def parse_request_body(request):
    """Utility function to parse JSON request body."""
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'message': 'CSRF cookie set'})


@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Validate input
            if not username or not password:
                return JsonResponse({
                    'error': 'Username and password are required'
                }, status=400)

            # Check if user exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'error': 'Username already exists'
                }, status=400)

            # Create user
            user = User.objects.create_user(
                username=username,
                password=password
            )
            
            return JsonResponse({
                'message': 'User created successfully',
                'user': {'username': user.username}
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)

    return JsonResponse({
        'error': 'Method not allowed'
    }, status=405)


@ensure_csrf_cookie
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    body = parse_request_body(request)
    if not body:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    username = body.get('username')
    password = body.get('password')

    if not username or not password:
        return JsonResponse({
            'error': 'Missing credentials',
            'details': {
                'username': 'provided' if username else 'required',
                'password': 'provided' if password else 'required'
            }
        }, status=400)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({
            'error': 'Authentication failed',
            'details': 'Invalid username or password'
        }, status=400)
        
    login(request, user)
    return JsonResponse({
        'message': 'Login successful',
        'user': {
            'username': user.username,
        }
    }, status=200)


@login_required
def current_user(request):
    user = request.user
    return JsonResponse({
        'username': user.username,
    })


@require_POST
@ensure_csrf_cookie
def logout_view(request):
    try:
        logout(request)
        return JsonResponse({'message': 'Déconnexion réussie'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
