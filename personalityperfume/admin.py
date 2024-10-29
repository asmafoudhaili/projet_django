# admin.py

from django.contrib import admin
from .models import PersonalityPerfume

@admin.register(PersonalityPerfume)
class PersonalityPerfumeAdmin(admin.ModelAdmin):
    list_display = ('personality_type', 'perfume_type')  # Affiche les types de personnalité et de parfum dans la liste
    search_fields = ('personality_type', 'perfume_type')  # Active la recherche par type de personnalité ou de parfum
    list_filter = ('perfume_type',)  # Ajoute un filtre pour trier par type de parfum