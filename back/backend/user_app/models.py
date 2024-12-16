from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Gestionnaire personnalisé pour la création d'utilisateurs
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hachage du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


# Modèle d'utilisateur personnalisé sans les champs supplémentaires
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Gestionnaire personnalisé pour ce modèle
    objects = CustomUserManager()

    # Spécifie que le champ username est utilisé pour l'authentification
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # Pas de champs obligatoires supplémentaires pour la création d'un superuser

    def __str__(self):
        return self.username

    # Ajout des méthodes nécessaires pour l'authentification
    @property
    def is_authenticated(self):
        return True  # Cela indique que l'utilisateur est authentifié

    @property
    def is_anonymous(self):
        return False  # Cela indique que l'utilisateur n'est pas anonyme

