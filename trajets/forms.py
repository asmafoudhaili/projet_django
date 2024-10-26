from django import forms
from .models import TrajetLivraison

class TrajetLivraisonForm(forms.ModelForm):
    class Meta:
        model = TrajetLivraison
        fields = ['livraison', 'temps_estime', 'points_traffic']
