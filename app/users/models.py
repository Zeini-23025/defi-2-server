from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('Moderateur', 'Modérateur'),
        ('contributor', 'Contributeur'),
    ]
    username = None 
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=255, blank=False, null=False)  
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='contributor')

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['nom']  

    def __str__(self):
        return self.email


class OTP(models.Model):
    email = models.EmailField()  
    code = models.CharField(max_length=6, unique=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        expiration_time = self.created_at + timedelta(minutes=5)
        return not self.is_used and timezone.now() <= expiration_time

    def __str__(self):
        return f"OTP for {self.email}: {self.code}"
