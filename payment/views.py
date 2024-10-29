
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Commande, Paiement, CommandeArticle
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from sklearn.linear_model import LinearRegression
import ollama
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Utiliser un backend non interactif
import matplotlib.pyplot as plt
import base64
import io



def commande_detail(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'commande_detail.html', {'commande': commande})

def get_successful_payments():
    # Filtrer les paiements réussis
    paiements_reussis = Paiement.objects.filter(statut_paiement='réussi')
    # Extraire les informations pertinentes
    data = [
        {
            'date': paiement.date,
            'montant': paiement.commande.total
        }
        for paiement in paiements_reussis
    ]
    # Convertir en DataFrame pour un meilleur traitement des données
    df = pd.DataFrame(data)
    return df

def preprocess_data(df):
    # Convertir la colonne 'date' en format DateTime
    df['date'] = pd.to_datetime(df['date'])
    # Grouper par mois et calculer la somme des montants
    df['mois'] = df['date'].dt.to_period('M')
    monthly_data = df.groupby('mois')['montant'].sum().reset_index()
    return monthly_data

def predict_future_revenue(monthly_data):
    # Préparer les données pour l'entraînement
    X = monthly_data.index.values.reshape(-1, 1)  # Mois
    y = monthly_data['montant'].values  # Montant

    # Créer et entraîner le modèle de régression linéaire
    model = LinearRegression()
    model.fit(X, y)

    # Prédire pour le mois suivant
    next_month = [[len(X)]]  # Mois suivant
    predicted_revenue = model.predict(next_month)
    return predicted_revenue[0]

def interpret_prediction(predicted_revenue):
    prompt = f"The predicted revenue for next month is ${predicted_revenue:.2f}. Can you provide an analysis of this trend?"
    response = ollama.generate(model='mistral', prompt=prompt)
    return response

def display_revenue_prediction(request):
    df = get_successful_payments()
    monthly_data = preprocess_data(df)
    predicted_revenue = predict_future_revenue(monthly_data)
    interpretation = interpret_prediction(predicted_revenue)

    # Préparation des données pour le graphique
    monthly_labels = monthly_data['mois'].astype(str).tolist()  # Convertir les périodes en chaîne de caractères
    monthly_revenue = monthly_data['montant'].tolist()

    # Créer le graphique
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_labels, monthly_revenue, marker='o', label='Revenus Mensuels', color='blue')
    plt.axhline(y=predicted_revenue, color='green', linestyle='--', label='Prédiction Mois Suivant')
    plt.title('Prédiction des Revenus')
    plt.xlabel('Mois')
    plt.ylabel('Montant ($)')
    plt.legend()
    plt.grid(True)

    # Sauvegarder le graphique dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Convertir le buffer en image Base64
    graph = base64.b64encode(buf.getvalue()).decode('utf8')

    context = {
        'predicted_revenue': predicted_revenue,
        'interpretation': interpretation,
        'graph': graph,  # Ajouter l'image au contexte
    }
    return render(request, 'prediction.html', context)