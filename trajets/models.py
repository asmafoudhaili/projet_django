from django.db import models
from livraisons.models import Livraison

class TrajetLivraison(models.Model):
    livraison = models.OneToOneField(Livraison, on_delete=models.CASCADE, related_name='trajet')
    temps_estime = models.DurationField()
    points_traffic = models.JSONField()  # Utilisé pour stocker les données de trafic sous forme JSON

    def __str__(self):
        return f"Trajet pour {self.livraison.commande} avec temps estimé {self.temps_estime}"
