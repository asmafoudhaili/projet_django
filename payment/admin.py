from django.contrib import admin

from .models import Commande, Paiement, CommandeArticle


class CommandeArticleInline(admin.TabularInline):
    model = CommandeArticle
    extra = 1  # Permet d'ajouter plusieurs articles
@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('client', 'total', 'statut')
    search_fields = ('client__username',)
    list_filter = ('statut',)
    inlines = [CommandeArticleInline]  # Ajoute les articles inline dans le formulaire de commande

    def save_model(self, request, obj, form, change):
        # Enregistrez l'objet commande pour obtenir une clé primaire
        super().save_model(request, obj, form, change)
        
        # Calculez le total après l'enregistrement de la commande
        total = sum(
            item.parfum.prix * item.quantite
            for item in obj.commandearticle_set.all()
        )
        
        # Mettez à jour le total de la commande
        obj.total = total
        obj.save()

@admin.register(Paiement)  
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('commande', 'methode_paiement', 'statut_paiement', 'date')
    search_fields = ('commande__client__username',)
    list_filter = ('statut_paiement',)