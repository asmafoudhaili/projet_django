from django.db import models

class Livraison(models.Model):
    GOUVERNORATS = [
        ('Ariana', 'Ariana'),
        ('Béja', 'Béja'),
        ('Ben Arous', 'Ben Arous'),
        ('Bizerte', 'Bizerte'),
        ('Gabès', 'Gabès'),
        ('Gafsa', 'Gafsa'),
        ('Jendouba', 'Jendouba'),
        ('Kairouan', 'Kairouan'),
        ('Kasserine', 'Kasserine'),
        ('Kébili', 'Kébili'),
        ('Le Kef', 'Le Kef'),
        ('Mahdia', 'Mahdia'),
        ('La Manouba', 'La Manouba'),
        ('Médenine', 'Médenine'),
        ('Monastir', 'Monastir'),
        ('Nabeul', 'Nabeul'),
        ('Sfax', 'Sfax'),
        ('Sidi Bouzid', 'Sidi Bouzid'),
        ('Siliana', 'Siliana'),
        ('Sousse', 'Sousse'),
        ('Tataouine', 'Tataouine'),
        ('Tozeur', 'Tozeur'),
        ('Tunis', 'Tunis'),
        ('Zaghouan', 'Zaghouan'),
    ]

    commande = models.CharField(max_length=100)
    adresse_livraison = models.CharField(max_length=255, choices=GOUVERNORATS)
    statut_livraison = models.CharField(max_length=50)
    transporteur = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.commande} - {self.statut_livraison}"
