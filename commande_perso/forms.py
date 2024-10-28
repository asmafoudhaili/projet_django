# commande_perso/forms.py
from django import forms
from .models import CustomizationOption, CustomOrder

class CustomizationOptionForm(forms.ModelForm):
    class Meta:
        model = CustomizationOption
        fields = ['customization_type', 'details']

class CustomOrderForm(forms.ModelForm):
    engraving_text = forms.CharField(required=False, label="Engraving Text")
    fragrance_choice = forms.CharField(required=False, label="Fragrance Choice")
    
    # Change these fields to CharField for regular text input
    base_notes = forms.CharField(required=True, label="Base Notes")
    middle_notes = forms.CharField(required=True, label="Middle Notes")
    top_notes = forms.CharField(required=True, label="Top Notes")
    
    fragrance_strength = forms.ChoiceField(choices=[
        ('eau de toilette', 'Eau de Toilette'),
        ('eau de parfum', 'Eau de Parfum'),
        # Other strengths can be added here
    ], required=True, label="Fragrance Strength")
    
    number_of_bottles = forms.IntegerField(min_value=1, initial=1, label="Number of Bottles")
    additional_notes = forms.CharField(widget=forms.Textarea, required=False, label="Additional Notes")

    class Meta:
        model = CustomOrder
        fields = ['base_notes', 'middle_notes', 'top_notes', 'fragrance_strength', 'number_of_bottles', 'engraving_text', 'fragrance_choice', 'additional_notes']
