from django.db import models
from django.contrib.auth.models import User  # Import du modèle User de Django
from perfumes.models import Perfume

class Commande(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)  # Relation avec User
    articles = models.ManyToManyField(Perfume, through='CommandeArticle')  # Relation ManyToMany avec un modèle intermédiaire
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')

    def __str__(self):
        return f"Commande de {self.client.username} - Total : {self.total}"

class CommandeArticle(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    parfum = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} x {self.parfum.nom} dans la commande {self.commande.id}"

class Paiement(models.Model):
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE)
    methode_paiement = models.CharField(max_length=50)  
    STATUT_PAIEMENT_CHOICES = [
        ('en_attente', 'En attente'),
        ('réussi', 'Réussi'),
        ('échoué', 'Échoué'),
    ]
    statut_paiement = models.CharField(max_length=20, choices=STATUT_PAIEMENT_CHOICES, default='en_attente')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement pour {self.commande.client.username} - Statut : {self.statut_paiement}"
