# commande_perso/forms.py
from django import forms
from .models import CustomizationOption, CustomOrder

class CustomizationOptionForm(forms.ModelForm):
    class Meta:
        model = CustomizationOption
        fields = ['customization_type', 'details']

class CustomOrderForm(forms.ModelForm):
    engraving_text = forms.CharField(required=False, label="Engraving Text")  # Champ optionnel pour l'engravement
    fragrance_choice = forms.CharField(required=False, label="Fragrance Choice")  # Champ optionnel pour la fragrance
    base_notes = forms.ChoiceField(choices=[
        ('sandalwood', 'Sandalwood'),
        ('vanilla', 'Vanilla'),
        # Ajoutez d'autres notes de base ici
    ], required=True, label="Base Notes")
    middle_notes = forms.ChoiceField(choices=[
        ('rose', 'Rose'),
        ('jasmine', 'Jasmine'),
        # Ajoutez d'autres notes de coeur ici
    ], required=True, label="Middle Notes")
    top_notes = forms.ChoiceField(choices=[
        ('citrus', 'Citrus'),
        ('mint', 'Mint'),
        # Ajoutez d'autres notes de tête ici
    ], required=True, label="Top Notes")
    fragrance_strength = forms.ChoiceField(choices=[
        ('eau de toilette', 'Eau de Toilette'),
        ('eau de parfum', 'Eau de Parfum'),
        # Ajoutez d'autres forces de fragrance ici
    ], required=True, label="Fragrance Strength")
    number_of_bottles = forms.IntegerField(min_value=1, initial=1, label="Number of Bottles")  # Champ pour le nombre de bouteilles
    additional_notes = forms.CharField(widget=forms.Textarea, required=False, label="Additional Notes")  # Notes supplémentaires

    class Meta:
        model = CustomOrder
        fields = ['base_notes', 'middle_notes', 'top_notes', 'fragrance_strength', 'number_of_bottles', 'engraving_text', 'fragrance_choice', 'additional_notes']
