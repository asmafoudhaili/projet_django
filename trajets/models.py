from django.db import models
from livraisons.models import Livraison

class TrajetLivraison(models.Model):
    POINT_DEPART_CHOICES = [
        ('Tunis', 'Tunis'),
        ('Sfax', 'Sfax'),
    ]

    livraison = models.OneToOneField(Livraison, on_delete=models.CASCADE, related_name='trajet')
    temps_estime = models.DurationField()
    point_de_depart = models.CharField(max_length=255, choices=POINT_DEPART_CHOICES, default="Tunis")
    point_d_arrivee = models.CharField(max_length=255, blank=True)  # Allow blank so we can set it in save()

    def save(self, *args, **kwargs):
        if not self.point_d_arrivee and self.livraison:
            self.point_d_arrivee = self.livraison.adresse_livraison  # Automatically set to `adresse_livraison`
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Trajet pour {self.livraison.commande} avec temps estimé {self.temps_estime} de {self.point_de_depart} à {self.point_d_arrivee}"
