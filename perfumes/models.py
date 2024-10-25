from django.db import models
import json

# Create your models here.
class PerfumeImage(models.Model):
    image_file = models.ImageField(upload_to='perfume_images/')

    def __str__(self):
        return f'Image {self.id}'

class Perfume(models.Model):
    # Informations de base
    nom = models.CharField(max_length=100)  # Nom du parfum
    marque = models.CharField(max_length=100)  # Marque du parfum
    type = models.CharField(max_length=100)  # Type de parfum (e.g., Eau de Parfum)
    contenance = models.CharField(max_length=100)  # Contenance (e.g., 100ml)
    prix = models.DecimalField(max_digits=10, decimal_places=2)  # Prix du parfum
    disponibilite = models.BooleanField(default=True)  # Disponibilité du produit
    quantite = models.PositiveIntegerField()  # Quantité disponible
    image = models.ImageField(upload_to='perfume_images/')  # Image du produit
    
    # Notes olfactives
    notes_de_tete = models.TextField(blank=True, null=True)  # Notes de tête (e.g., Fruity, Floral)
    notes_de_coeur = models.TextField(blank=True, null=True)  # Notes de cœur (e.g., Floral, Spicy)
    notes_de_fond = models.TextField(blank=True, null=True)  # Notes de fond (e.g., Musky, Woody)

    # Informations supplémentaires
    ingredients = models.TextField()  # Liste des ingrédients (e.g., Alcohol, Water)
    utilisation = models.TextField(blank=True, null=True)  # Instructions d'utilisation
    details_de_fabrication = models.CharField(max_length=255, blank=True, null=True)  # Détails de fabrication
    code_barres = models.CharField(max_length=13, blank=True, null=True)  # Numéro de code-barres
    avertissements = models.TextField(blank=True, null=True)  # Avertissements et précautions

    # Design et apparence
    design = models.CharField(max_length=255, blank=True, null=True)  # Détails du design (e.g., Vintage bottle)
    forme = models.CharField(max_length=100, blank=True, null=True)  # Forme de la bouteille (e.g., rectangulaire)
    couleur = models.CharField(max_length=100, blank=True, null=True)  # Couleur de la bouteille et de l'emballage
    
    # Méta-informations
    description_forme_couleur = models.TextField(blank=True, null=True)  # Description de la forme et de la couleur

    def __str__(self):
        return f"{self.nom} - {self.marque}"


class Description(models.Model):
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, related_name='description')
    description = models.JSONField()

    def __str__(self):
        return f"Description for {self.perfume.nom}"
