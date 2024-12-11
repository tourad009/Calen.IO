from django.shortcuts import render, redirect
from django.contrib import messages
from .models import user
from .forms import UserRegisterForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Replace with your login page name
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate user (basic check since no hashing is used)
            try:
                user_instance = user.objects.get(username=username, password=password)
                # Example of setting session:
                request.session['user_id'] = user_instance.id
                messages.success(request, 'You are now logged in.')
                return redirect('home')  # Replace with your home page name
            except user.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})
