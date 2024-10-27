# models.py
from django.db import models

class PersonalityPerfume(models.Model):
    personality_type = models.CharField(max_length=50, unique=True)  # E.g., "Rêveur (Imagineur)"
    perfume_type = models.CharField(max_length=100)  # E.g., "Floral", "Woody", etc.
    characteristics = models.TextField()  # Describe the characteristics of the perfume

    def __str__(self):
        return f"{self.personality_type} - {self.perfume_type}"
