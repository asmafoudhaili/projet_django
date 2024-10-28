from django.contrib import admin, messages
from .models import Cart, CartItem
from decimal import Decimal

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'item_count', 'total_amount')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
    actions = ['apply_discount', 'clear_cart_items']

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Nombre d\'articles'

    def total_amount(self, obj):
        total = sum(item.get_subtotal() for item in obj.items.all())
        return f"{total:.2f} €"
    total_amount.short_description = 'Montant total'

    # Action pour appliquer une réduction
    def apply_discount(self, request, queryset):
        discount_rate = Decimal('0.10')  # 10% de réduction en utilisant Decimal pour éviter les conflits de type
        for cart in queryset:
            for item in cart.items.all():
                item.custom_order.total_amount *= (Decimal('1.0') - discount_rate)
                item.custom_order.save()
        self.message_user(request, f"Réduction de {discount_rate * 100}% appliquée avec succès.", messages.SUCCESS)
    apply_discount.short_description = "Une réduction de 10%%"

    # Action pour vider les articles d'un panier
    def clear_cart_items(self, request, queryset):
        for cart in queryset:
            cart.items.all().delete()
        self.message_user(request, "Articles du panier supprimés avec succès.", messages.SUCCESS)
    clear_cart_items.short_description = "Vider les articles du panier sélectionné"

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'custom_order', 'quantity', 'subtotal')
    list_filter = ('cart',)
    search_fields = ('cart__user__username', 'custom_order__client__username')

    def subtotal(self, obj):
        return obj.get_subtotal()
    subtotal.short_description = 'Sous-total'

   
