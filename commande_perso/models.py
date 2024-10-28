from django.conf import settings
from django.db import models
from django.utils import timezone

class CustomizationOption(models.Model):
    TYPE_CHOICES = [
        ('ENGRAVING', 'Engraving'),
        ('FRAGRANCE_CHOICE', 'Fragrance Choice'),
    ]

    customization_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    details = models.TextField()

    def __str__(self):
        return f"{self.customization_type}: {self.details}"

class CustomOrder(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  # Rendre le champ nullable
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Rendre le champ nullable
    order_date = models.DateTimeField(default=timezone.now)  # Valeur par défaut ajoutée
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')  # Valeur par défaut

    # Nouveaux champs pour la personnalisation
    base_notes = models.CharField(max_length=100, blank=True, null=True)  # Ajout du champ base_notes
    middle_notes = models.CharField(max_length=50, blank=True, null=True)  # Notes de cœur, rendues optionnelles
    top_notes = models.CharField(max_length=50, blank=True, null=True)  # Notes de tête, rendues optionnelles
    fragrance_strength = models.CharField(max_length=50, blank=True, null=True)  # Force du parfum, rendue optionnelle
    number_of_bottles = models.PositiveIntegerField(default=1)  # Nombre de bouteilles
    engraving_text = models.CharField(max_length=100, blank=True, null=True)  # Texte d'engravement
    fragrance_choice = models.CharField(max_length=100, blank=True, null=True)  # Choix de la fragrance
    additional_notes = models.TextField(blank=True, null=True)  # Notes supplémentaires

    customization_options = models.ManyToManyField(CustomizationOption)

    def __str__(self):
        return f"Order {self.id} - {self.order_status}"
