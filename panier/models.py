from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    custom_order = models.ForeignKey('commande_perso.CustomOrder', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_subtotal(self):
        return self.custom_order.total_amount * self.quantity  # Calcul du sous-total


    def __str__(self):
        return f"{self.custom_order} (x{self.quantity})"
