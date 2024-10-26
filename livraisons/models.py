from django.db import models

class Livraison(models.Model):
    commande = models.CharField(max_length=100)
    adresse_livraison = models.CharField(max_length=255)
    statut_livraison = models.CharField(max_length=50)
    transporteur = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.commande} - {self.statut_livraison}"
