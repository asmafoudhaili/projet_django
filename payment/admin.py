from django.contrib import admin

from .models import Commande, Paiement

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('client', 'total', 'statut')
    search_fields = ('client__username',)
    list_filter = ('statut',)

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('commande', 'methode_paiement', 'statut_paiement', 'date')
    search_fields = ('commande__client__username',)
    list_filter = ('statut_paiement',)