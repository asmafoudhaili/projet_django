import logging
from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from payment.models import Paiement,Commande
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
import stripe
from django.conf import settings

# Configuration du logger
logger = logging.getLogger(__name__)

@login_required
def cart_list(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart_items = []

    # Calcul des sous-totaux des articles dans le panier
    items_with_subtotals = []
    for item in cart_items:
        subtotal = item.get_subtotal()
        items_with_subtotals.append({
            'item': item,
            'subtotal': subtotal
        })

    # Total des articles du panier
    cart_total = sum(item['subtotal'] for item in items_with_subtotals)

    # Récupération des commandes existantes pour l'utilisateur
    commandes = Commande.objects.filter(client=request.user)

    # Calcul du total des commandes existantes
    commandes_total = commandes.aggregate(total=Sum('total'))['total'] or 0.00

    # Calcul du total combiné
    total_general = cart_total + commandes_total

    context = {
        'cart_items': items_with_subtotals,
        'cart_total': cart_total,
        'commandes': commandes,
        'commandes_total': commandes_total,
        'total_general': total_general,
    }
    return render(request, 'panier.html', context)

def update_cart_item(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity < 1:
            cart_item.quantity = 1

    cart_item.save()

    subtotal = cart_item.get_subtotal()
    cart_total = sum(item.get_subtotal() for item in CartItem.objects.filter(cart=cart_item.cart))

    # Debugging logs
    logger.debug(f'Updated CartItem: {cart_item}, Subtotal: {subtotal}, Cart Total: {cart_total}')

    return JsonResponse({
        'subtotal': float(subtotal),
        'cart_total': float(cart_total),
        'quantity': cart_item.quantity,
    })



@login_required
def cart_remove_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    item.delete()
    
    # Calculer le nouveau total du panier après la suppression de l'item
    cart_total = sum(cart_item.item.total_amount * cart_item.quantity for cart_item in cart.items.all())

    return JsonResponse({'success': True, 'cart_total': cart_total})


stripe.api_key = settings.STRIPE_SECRET_KEY

@require_POST
def create_checkout_session(request):
    total_combined = float(request.POST.get('total_combined', 0))
    
    # Créer une commande pour enregistrer le paiement
    commande = Commande.objects.create(client=request.user, total=total_combined)

    # Enregistrer le paiement dans la base de données avant de créer la session Stripe
    paiement = Paiement.objects.create(
        commande=commande,
        methode_paiement='Stripe',  # Ajustez selon vos besoins
    )

    # Créer des articles de ligne pour Stripe
    line_items = [{
        'price_data': {
            'currency': 'usd',  # Remplacez par votre devise
            'product_data': {
                'name': 'Total des Commandes',  # Nom générique pour le total
            },
            'unit_amount': int(total_combined * 100),  # Montant en cents
        },
        'quantity': 1,  # Quantité de 1 pour le total
    }]
    

    # Créer une session de paiement Stripe
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://localhost:8000/cart/success/',  # URL de succès
        cancel_url='http://localhost:8000/cart/cancel/',    # URL d'annulation
    )

    # Mettre à jour le statut du paiement après la création de la session
    paiement.statut_paiement = 'en_attente'  # Statut initial
    paiement.save()

    # Rediriger l'utilisateur vers la session de paiement Stripe
    return redirect(checkout_session.url, code=303)

# Vues pour les pages de succès et d'annulation
def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')
def delete_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    commande.delete()  
    return JsonResponse({'success': True})