from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('csrf/', views.csrf, name='csrf'),
    path('current/', views.current_user, name='current_user'),
    path('logout/', views.logout_view, name='logout'),
]