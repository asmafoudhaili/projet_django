# forms.py

from django import forms
from .models import Perfume
from .models import Description

class PerfumeImageUploadForm(forms.Form):
    image = forms.ImageField()

class PerfumeForm(forms.ModelForm):
    class Meta:
        model = Perfume
        fields = ['nom', 'marque', 'type', 'contenance', 'prix', 'disponibilite', 'quantite', 'image']

class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ['perfume', 'description']