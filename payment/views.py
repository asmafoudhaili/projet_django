
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Commande, Paiement, CommandeArticle
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request, commande_id):
    if request.method == 'POST':  # Vérifiez que c'est une requête POST
        try:
            commande = Commande.objects.get(id=commande_id)

            # Créez la session de paiement Stripe
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Commande {commande.id}',
                        },
                        'unit_amount': int(commande.total * 100),  # Montant en centimes
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/payment/success/'),
                cancel_url=request.build_absolute_uri('/payment/cancel/'),
            )
            return JsonResponse({'id': checkout_session.id})  # Retourne l'ID de la session
        except Commande.DoesNotExist:
            return JsonResponse({'error': 'Commande not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST requests are accepted.'}, status=400) 

def success_view(request):
    return render(request, 'payment/success.html')

def cancel_view(request):
    return render(request, 'payment/cancel.html')

