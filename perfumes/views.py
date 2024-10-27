# views.py
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PerfumeImageUploadForm, PerfumeForm
import pandas as pd
import os
from io import BytesIO
from PIL import Image
from ollama import generate
from .models import Perfume, Description
import json
import spacy
nlp = spacy.load("en_core_web_sm")  # Or the appropriate model for your language

# Chargement ou création du fichier CSV pour sauvegarder les descriptions
def load_or_create_dataframe(filename):
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=['image_file', 'description'])
    return df

df = load_or_create_dataframe('image_descriptions.csv')

def process_image(image_file, df):
    # Charger l'image et la convertir en bytes pour le modèle
    with Image.open(image_file) as img:
        with BytesIO() as buffer:
            img.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()

    full_response = ''

    prompt = """
Please describe the perfume image you are analyzing and provide the details in the following format as a list of lists:

{
    Nom: Name of the perfume,
    Marque: Brand name,
    Type: Type of perfume (e.g. Eau de Parfum, Eau de Toilette),
    Contenance: Volume in ml or fl oz,
    Notes_de_Tête: ["Top notes (e.g. Fruity, Floral)"],
    Notes_de_Coeur: ["Heart notes (e.g. Floral, Spicy)"],
    Notes_de_Fond: ["Base notes (e.g. Musky, Woody)"],
    Ingrédients: ["List of ingredients (e.g. Alcohol, Water, Perfume)"],
    Utilisation: "Usage instructions (if available)",
    Détails_de_Fabrication: Details of production (e.g. Made in France),
    Code_Barres: Barcode number (if available),
    Avertissements: "Warnings and precautions (e.g. Avoid contact with eyes),
    Design: Design details (e.g. Vintage bottle with floral patterns),
    Forme: Shape of the bottle (e.g. rectangular, round, curved),
    Couleur: "Colors of the bottle and packaging (e.g. gold, pink, transparent),
    Description_Forme_Couleur "Describe the overall form and color of the perfume bottle and packaging in more detail (e.g. the bottle has a sleek, curved shape with a pink-tinted glass and a golden cap)"
}


Fill in the details as accurately as possible based on the image you are analyzing, including descriptions of the bottle’s shape and coloration.
"""
    # Envoyer l'image au modèle LLaVA pour obtenir la description
    for response in generate(model='llava', 
                             prompt=prompt,
                             images=[image_bytes], 
                             stream=True):
        full_response += response['response']
    
    # Sauvegarder la description dans le DataFrame
    df.loc[len(df)] = [image_file.name, full_response]
    df.to_csv('image_descriptions.csv', index=False)  # Mise à jour du CSV

    return full_response


def recommanded_process_image(image_file):
    # Charger l'image et la convertir en bytes pour le modèle
    with Image.open(image_file) as img:
        with BytesIO() as buffer:
            img.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()

    full_response = ''

    prompt = """
Please describe the perfume image you are analyzing and provide the details in the following :
Nom,Marque,Type,Contenance,Notes_de_Tête,Notes_de_Coeur,Notes_de_Fond,Ingrédients,Design,Forme,Description_Forme_Couleu
Fill in the details as accurately as possible based on the image you are analyzing, including descriptions of the bottle’s shape and coloration.
"""
    # Envoyer l'image au modèle LLaVA pour obtenir la description
    for response in generate(model='llava', 
                             prompt=prompt,
                             images=[image_bytes], 
                             stream=True):
        full_response += response['response']
    
    return full_response





def upload_image(request):
    if request.method == 'POST':
        form = PerfumeImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']

            # Process the uploaded image to get the description
            description = recommanded_process_image(image)  # Generate the description from the image
            matching_perfumes = compare_with_database(description)  # Compare with the database

            # Prepare to display the description and any matching perfumes
            return render(request, 'upload.html', {
                'form': form,
                'description': description,
                'matching_perfumes': matching_perfumes  # Pass matching perfumes to the template
            })
    else:
        form = PerfumeImageUploadForm()

    return render(request, 'upload.html', {'form': form})



def compare_with_database(description):
    # Parse the description with SpaCy
    doc = nlp(description)
    
    # Extract keywords and create a set of tokens from the description
    description_tokens = set(token.lemma_.lower() for token in doc if not token.is_stop)

    # Initialize a list for scoring
    scores = []

    # Fetch all perfumes from the database
    perfumes = Perfume.objects.all()
    
    for perfume in perfumes:
        # Concatenate attributes into a single string
        perfume_attributes = f"{perfume.nom} {perfume.marque} {perfume.type} " \
                             f"{perfume.contenance} {perfume.notes_de_tete} " \
                             f"{perfume.notes_de_coeur} {perfume.notes_de_fond} " \
                             f"{perfume.ingredients} {perfume.design} {perfume.forme}"
        
        # Tokenize the concatenated perfume attributes
        perfume_doc = nlp(perfume_attributes)
        perfume_tokens = set(token.lemma_.lower() for token in perfume_doc if not token.is_stop)

        # Calculate similarity score using Jaccard similarity
        intersection = description_tokens.intersection(perfume_tokens)
        union = description_tokens.union(perfume_tokens)
        jaccard_score = len(intersection) / len(union) if len(union) > 0 else 0
        
        scores.append((perfume, jaccard_score))

    # Sort perfumes by score in descending order and get the top 2
    top_matches = sorted(scores, key=lambda x: x[1], reverse=True)[:2]
    
    return [match[0] for match in top_matches]  # Return only the matching perfumes

def is_admin(user):
    return user.is_authenticated and user.is_staff  # Vérifie si l'utilisateur est authentifié et un membre du personnel


@user_passes_test(is_admin, login_url='/login/')  # Rediriger vers la page de connexion si non autorisé
def create_perfume(request):
    if request.method == 'POST':
        form = PerfumeForm(request.POST, request.FILES)
        if form.is_valid():
            # Créer un parfum
            new_perfume = form.save()
            
            # Analyser l'image et obtenir la description
            image_file = request.FILES['image']  # Récupérer l'image du formulaire
            description_text = process_image(image_file, df)  # Appeler la fonction pour analyser l'image
            
            # Créer une nouvelle description
            Description.objects.create(perfume=new_perfume, description=description_text)
            
            return redirect('perfume_list')  # Redirigez vers la liste des parfums ou une autre page
    else:
        form = PerfumeForm()

    return render(request, 'create_perfume.html', {'form': form})

def perfume_list(request):
    # Récupérer tous les objets Perfume
    perfumes = Perfume.objects.all()
    # Passer la liste de parfums au template
    return render(request, 'perfume_list.html', {'perfumes': perfumes})


# Détails d'un parfum
def perfume_detail(request, perfume_id):
    perfume = get_object_or_404(Perfume, id=perfume_id)
    description = Description.objects.get(perfume=perfume)  # Obtenir la description associée
    return render(request, 'perfume_detail.html', {'perfume': perfume, 'description': description})

# Modifier un parfum
def perfume_update(request, perfume_id):
    perfume = get_object_or_404(Perfume, id=perfume_id)
    if request.method == 'POST':
        form = PerfumeForm(request.POST, request.FILES, instance=perfume)
        if form.is_valid():
            form.save()
            return redirect('perfume_detail', perfume_id=perfume.id)
    else:
        form = PerfumeForm(instance=perfume)
    return render(request, 'perfume_form.html', {'form': form})

# Supprimer un parfum
def perfume_delete(request, perfume_id):
    perfume = get_object_or_404(Perfume, id=perfume_id)
    if request.method == 'POST':
        perfume.delete()
        return redirect('perfume_list')
    return render(request, 'perfume_confirm_delete.html', {'perfume': perfume})
