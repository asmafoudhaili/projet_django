from django import forms
from .models import Livraison

class LivraisonForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ['commande', 'adresse_livraison', 'statut_livraison', 'transporteur']
