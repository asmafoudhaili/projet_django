from django.contrib import admin
from .models import Perfume, Description

# Enregistrer le modèle Perfume dans l'administration
class PerfumeAdmin(admin.ModelAdmin):
    # Affiche tous les champs du modèle Perfume dans l'interface d'administration
    fields = (
        'nom', 
        'marque', 
        'type', 
        'contenance', 
        'prix', 
        'disponibilite', 
        'quantite', 
        'image', 
        'notes_de_tete', 
        'notes_de_coeur', 
        'notes_de_fond', 
        'ingredients', 
        'utilisation', 
        'details_de_fabrication', 
        'code_barres', 
        'avertissements', 
        'design', 
        'forme', 
        'couleur', 
        'description_forme_couleur'
    )
    
    # Changer les champs à afficher dans la liste
    list_display = (
        'nom', 
        'marque', 
        'type', 
        'prix', 
        'disponibilite', 
        'quantite'
    )
    
    # Champs qui peuvent être recherchés
    search_fields = ('nom', 'marque', 'type')  
    
    # Filtres disponibles dans l'interface
    list_filter = ('disponibilite', 'type')  

# Enregistrer le modèle Description dans l'administration
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('perfume',)  # Affiche le parfum associé
    search_fields = ('perfume__nom',)  # Recherche par nom de parfum

# Enregistrer les modèles
admin.site.register(Perfume, PerfumeAdmin)
admin.site.register(Description, DescriptionAdmin)
