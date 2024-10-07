from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Ajoutez des champs personnalisés si nécessaire
    bio = models.TextField(blank=True, null=True, help_text="Biographie de l'utilisateur.")

    def __str__(self):
        return self.username
