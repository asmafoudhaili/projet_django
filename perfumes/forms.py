# forms.py

from django import forms
from .models import Perfume

class PerfumeImageUploadForm(forms.Form):
    image = forms.ImageField()

class PerfumeForm(forms.ModelForm):
    class Meta:
        model = Perfume
        fields = ['nom', 'marque', 'type', 'contenance', 'prix', 'disponibilite', 'quantite', 'image']