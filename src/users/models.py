from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
import random

class CustomUserManager(BaseUserManager):
  def create_user(self, username, email, password=None, **extra_fields):
    if not email:
      raise ValueError('The Email field must be set')
    email = self.normalize_email(email)
    user = self.model(username=username, email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, email,  password=None, **extra_fields):
    username = input("username: ") 

    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')
    
    return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
  email = models.EmailField(unique=True)
  username = models.CharField(
    max_length=150, 
    unique=True,
    validators=[],
  )
  ava = models.ImageField(upload_to="images/users/avas/", null=True)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def save(self, *args, **kwargs):
    if not self.pk:
      self.account = f'103012{random.randint(1000000000, 9999999999)}'

    super().save(*args, **kwargs)

  def __str__(self):
    return self.username