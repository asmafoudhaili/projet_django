from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem
from commande_perso.models import CustomOrder  # Assurez-vous d'importer le modèle de commande personnalisée
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

def cart_list(request):
    try:
        # Récupérez le panier de l'utilisateur connecté
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()  # Récupérer les items du panier
    except Cart.DoesNotExist:
        cart_items = []  # Si le panier n'existe pas, pas d'items

    # Passer les articles du panier au template
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'panier.html', context)

@login_required
def cart_item_count(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        count = sum(item.quantity for item in cart.items.all())
    else:
        count = 0
    return JsonResponse({'count': count})