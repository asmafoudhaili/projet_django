# commande_perso/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomizationOption, CustomOrder
from .forms import CustomizationOptionForm, CustomOrderForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from panier.models import Cart, CartItem 

# CustomizationOption Views
def customization_option_list(request):
    options = CustomizationOption.objects.all()
    return render(request, 'customization_option_list.html', {'options': options})

def customization_option_create(request):
    if request.method == 'POST':
        form = CustomizationOptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customization_option_list')
    else:
        form = CustomizationOptionForm()
    return render(request, 'customization_option_form.html', {'form': form})

def customization_option_update(request, pk):
    option = get_object_or_404(CustomizationOption, pk=pk)
    if request.method == 'POST':
        form = CustomizationOptionForm(request.POST, instance=option)
        if form.is_valid():
            form.save()
            return redirect('customization_option_list')
    else:
        form = CustomizationOptionForm(instance=option)
    return render(request, 'customization_option_form.html', {'form': form})

def customization_option_delete(request, pk):
    option = get_object_or_404(CustomizationOption, pk=pk)
    if request.method == 'POST':
        option.delete()
        return redirect('customization_option_list')
    return render(request, 'customization_option_confirm_delete.html', {'option': option})

# CustomOrder Views
def custom_order_list(request):
    orders = CustomOrder.objects.all()
    return render(request, 'custom_order_list.html', {'orders': orders})


def calculate_price(custom_order):
    # Coûts de base
    base_price_per_bottle = 20  # Prix de base par bouteille
    ingredient_cost = 0

    # Coûts en fonction des notes de parfum
    if custom_order.base_notes:
        ingredient_cost += 5  # Coût supplémentaire pour la base notes
    if custom_order.middle_notes:
        ingredient_cost += 3  # Coût supplémentaire pour les notes de cœur
    if custom_order.top_notes:
        ingredient_cost += 2  # Coût supplémentaire pour les notes de tête
    
    # Coût de la force du parfum
    if custom_order.fragrance_strength:
        ingredient_cost += 4  # Coût supplémentaire pour la force du parfum

    # Coût pour l'engravement
    engraving_cost = 5 if custom_order.engraving_text else 0

    # Coût pour le choix de la fragrance
    if custom_order.fragrance_choice:
        ingredient_cost += 7  # Coût supplémentaire pour le choix de la fragrance

    # Calcul du prix total
    total_price = (base_price_per_bottle + ingredient_cost + engraving_cost) * custom_order.number_of_bottles
    return total_price


@login_required
def custom_order_create(request):
    if request.method == 'POST':
        # Vérifiez si les données sont au format JSON
        if request.content_type == 'application/json':
            data = json.loads(request.body)  # Charge les données JSON
        else:
            data = request.POST  # Utilisez les données du formulaire si ce n'est pas du JSON

        form = CustomOrderForm(data)
        if form.is_valid():
            custom_order = form.save(commit=False)
            custom_order.client = request.user  # Associe automatiquement l’utilisateur connecté
            
            # Calcul du prix estimé
            estimated_price = calculate_price(custom_order)
            print(estimated_price)  # Vérifie si le prix est correct
            
            # Assigner le prix estimé au champ total_amount
            custom_order.total_amount = estimated_price
            
            # Enregistrer la commande
            custom_order.save()

            # Ajouter la commande au panier
            cart, created = Cart.objects.get_or_create(user=request.user)  # Récupérer ou créer le panier
            cart_item, created = CartItem.objects.get_or_create(cart=cart, custom_order=custom_order)
            if not created:
                cart_item.quantity += 1  # Si l'article est déjà dans le panier, incrémente la quantité
                cart_item.save()

            return JsonResponse({
                'success': True,
                'order_id': custom_order.id,
                'estimated_price': estimated_price,
                'order_details': {
                    'base_notes': custom_order.base_notes,
                    'middle_notes': custom_order.middle_notes,
                    'top_notes': custom_order.top_notes,
                    'fragrance_strength': custom_order.fragrance_strength,
                    'number_of_bottles': custom_order.number_of_bottles,
                    'engraving_text': custom_order.engraving_text,
                    'fragrance_choice': custom_order.fragrance_choice,
                }
            })
        else:
            return JsonResponse({'success': False, 'error': form.errors})

    # Si la méthode est GET, renvoie le formulaire de commande
    else:
        form = CustomOrderForm()
        return render(request, 'custom_order_form.html', {'form': form})



def custom_order_update(request, pk):
    order = get_object_or_404(CustomOrder, pk=pk)
    if request.method == 'POST':
        form = CustomOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('custom_order_list')
    else:
        form = CustomOrderForm(instance=order)
    return render(request, 'custom_order_form.html', {'form': form})

def custom_order_delete(request, pk):
    order = get_object_or_404(CustomOrder, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('custom_order_list')
    return render(request, 'custom_order_confirm_delete.html', {'order': order})