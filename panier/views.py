import logging
from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Configuration du logger
logger = logging.getLogger(__name__)

@login_required
def cart_list(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart_items = []

    # Calcul des sous-totaux et du total
    items_with_subtotals = []
    for item in cart_items:
        subtotal = item.custom_order.total_amount * item.quantity  # Calcul du sous-total
        items_with_subtotals.append({
            'item': item,
            'subtotal': subtotal
        })

    cart_total = sum(item['subtotal'] for item in items_with_subtotals)

    context = {
        'cart_items': items_with_subtotals,
        'cart_total': cart_total,
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



