from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
from simple_history.admin import SimpleHistoryAdmin
import pandas as pd
import csv
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomOrder

@admin.register(CustomOrder)
class CustomOrderAdmin(SimpleHistoryAdmin):
    list_display = (
        'client',
        'total_amount',
        'order_date',
        'order_status',
        'colored_status',
        'days_since_order',
    )
    list_filter = (
        'order_status',
        'order_date',
    )
    search_fields = ('client__username', 'order_status')
    list_editable = ('order_status', 'total_amount')
    readonly_fields = ('total_amount_preview',)
    actions = ['mark_as_shipped', 'cancel_order', 'export_as_csv', 'apply_discount', 'export_as_excel']

    def mark_as_shipped(self, request, queryset):
        queryset.update(order_status='shipped')
        self.message_user(request, "Les commandes sélectionnées ont été marquées comme expédiées.")
    mark_as_shipped.short_description = "Marquer comme expédié"

    def cancel_order(self, request, queryset):
        queryset.update(order_status='canceled')
        self.message_user(request, "Les commandes sélectionnées ont été annulées.")
    cancel_order.short_description = "Annuler la commande"

    def apply_discount(self, request, queryset):
        for order in queryset:
            if order.total_amount > 100:
                discounted_amount = order.total_amount * 0.9  # Applique une remise de 10 %
                order.total_amount = discounted_amount
                order.save(update_fields=['total_amount'])  # Sauvegarde uniquement le champ total_amount
        self.message_user(request, "Remise appliquée avec succès aux commandes sélectionnées.")
    apply_discount.short_description = "Appliquer une remise de 10 %%"

   

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        writer = csv.writer(response)
        writer.writerow(['Client', 'Montant total', 'Date', 'Statut'])
        for order in queryset:
            writer.writerow([order.client.username, order.total_amount, order.order_date, order.order_status])
        return response
    export_as_csv.short_description = "Exporter en CSV"

    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="orders.xlsx"'
        
        data = [
            [
                order.client.username,
                order.total_amount,
                order.order_date.replace(tzinfo=None) if order.order_date else '',  # Suppression du fuseau horaire
                order.order_status
            ]
            for order in queryset
        ]
        df = pd.DataFrame(data, columns=['Client', 'Montant Total', 'Date', 'Statut'])
        df.to_excel(response, index=False)
        
        return response
    export_as_excel.short_description = "Exporter en Excel"

    def colored_status(self, obj):
        if obj.order_status == 'shipped':
            return format_html('<span style="color: green;">✔ Expédié</span>')
        elif obj.order_status == 'canceled':
            return format_html('<span style="color: red;">✘ Annulé</span>')
        return format_html('<span style="color: orange;">En attente</span>')
    colored_status.short_description = 'Statut de commande'

    def total_amount_preview(self, obj):
        return f"{obj.total_amount} (prévisualisation)"
    total_amount_preview.short_description = "Montant total (prévisualisation)"

    def days_since_order(self, obj):
        delta = timezone.now().date() - obj.order_date.date() if obj.order_date else None
        return delta.days if delta else "Non disponible"
    days_since_order.short_description = "Jours écoulés"
