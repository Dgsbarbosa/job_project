from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom manager para o modelo de usuário sem username
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo Email deve ser preenchido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('O superusuário precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O superusuário precisa ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Adicionando novos campos ao modelo de usuário
    username = None
    email = models.EmailField(unique=True)
    last_updated = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=["first_name","last_name"]
    
    objects = CustomUserManager()
    def __str__(self):
        return self.email
