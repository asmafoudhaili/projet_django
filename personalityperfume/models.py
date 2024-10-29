# models.py
from django.db import models
from django.core.validators import MinLengthValidator

class PersonalityPerfume(models.Model):
    personality_type = models.CharField(
        max_length=50, 
        unique=True, 
        validators=[MinLengthValidator(3)]  # Minimum de 3 caractères
    )
    perfume_type = models.CharField(
        max_length=100, 
        validators=[MinLengthValidator(3)]  # Minimum de 3 caractères
    )
    characteristics = models.TextField()  # Décrire les caractéristiques du parfum

    def __str__(self):
        return f"{self.personality_type} - {self.perfume_type}"