
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Commande, Paiement, CommandeArticle
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

stripe.api_key = settings.STRIPE_SECRET_KEY

@require_POST
def create_checkout_session(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)

    # Enregistrer le paiement dans la base de données avant de créer la session Stripe
    paiement = Paiement.objects.create(
        commande=commande,
        methode_paiement='Stripe',  # Vous pouvez ajuster cela si vous avez plusieurs méthodes de paiement
    )

    # Créez les items de ligne pour Stripe
    line_items = []
    for article in commande.commandearticle_set.all():
        line_items.append({
            'price_data': {
                'currency': 'usd',  # Remplacez par votre devise
                'product_data': {
                    'name': article.parfum.nom,  # Remplacez par le nom de votre produit
                },
                'unit_amount': int(article.parfum.prix * 100),  # Montant en cents
            },
            'quantity': article.quantite,
        })

    # Créer une session de paiement Stripe
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://localhost:8000/payment/success/',  # URL de succès
        cancel_url='http://localhost:8000/payment/cancel/',    # URL d'annulation
    )

    # Mettre à jour le statut du paiement après la création de la session
    paiement.statut_paiement = 'en_attente'  # Statut initial
    paiement.save()

    # Rediriger l'utilisateur vers la session de paiement Stripe
    return redirect(checkout_session.url, code=303)
    # views.py

def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')


def commande_detail(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'commande_detail.html', {'commande': commande})