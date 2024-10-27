from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect

@login_required
def cart_list(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart_items = []

    items_with_subtotals = []
    for item in cart_items:
        subtotal = item.custom_order.total_amount * item.custom_order.number_of_bottles * item.quantity
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


@login_required
def cart_add_item(request, item_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product_id=item_id)
    item.quantity += 1
    item.save()
    return JsonResponse({'message': 'Item added successfully!'})

@login_required
def cart_remove_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=item_id)
    item.delete()  # Supprime complètement l'item du panier
    return JsonResponse({'message': 'Item removed successfully!'})

@login_required
def cart_item_count(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        count = sum(item.quantity for item in cart.items.all())
    else:
        count = 0
    return JsonResponse({'count': count})

@login_required
def update_cart_item(request, item_id, action):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=item_id)

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1

    item.save()

    # Calculer le nouveau sous-total
    subtotal = item.custom_order.total_amount * item.custom_order.number_of_bottles * item.quantity

    return JsonResponse({'message': 'Item updated successfully!', 'subtotal': subtotal})
