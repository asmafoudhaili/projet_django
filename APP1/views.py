# APP1/views.py
from django.shortcuts import render, redirect
from perfumes.models import Perfume
from perfumes.forms import PerfumeForm
from django.views.decorators.csrf import csrf_exempt
from payment.models import Commande, Paiement, CommandeArticle
import json
from django.http import JsonResponse



def index(request):
    perfumes = Perfume.objects.all()  # Récupérer tous les parfums
    form = None

    if request.method == "POST":
        form = PerfumeForm(request.POST, request.FILES)  # Traiter le formulaire
        if form.is_valid():
            form.save()  # Enregistrer le nouveau parfum
            return redirect('index')  # Rediriger vers la page d'accueil

    else:
        form = PerfumeForm()

    return render(request, 'index.html', {'perfumes': perfumes, 'form': form})

@csrf_exempt
def order_perfume(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            perfume_id = data.get('perfume_id')
            quantity = data.get('quantity', 1)

            # Vérifier que perfume_id est fourni
            if not perfume_id:
                return JsonResponse({'status': 'error', 'message': 'ID du parfum manquant'}, status=400)

            # Récupérer le parfum
            perfume = Perfume.objects.get(id=perfume_id)

            # Créer la commande
            commande = Commande.objects.create(
                client=request.user,  # Assurez-vous que l'utilisateur est connecté
                total=perfume.prix * quantity  # Calculer le total basé sur la quantité
            )

            # Ajouter le parfum à la commande via le modèle intermédiaire
            CommandeArticle.objects.create(commande=commande, parfum=perfume, quantite=quantity)

            return JsonResponse({'status': 'success', 'commande_id': commande.id})
        except Perfume.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Parfum non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Requête non autorisée'}, status=405)


