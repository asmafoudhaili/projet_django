# APP1/views.py
from django.shortcuts import render, redirect
from perfumes.models import Perfume
from perfumes.forms import PerfumeForm
from perfumes.models import Description  # Ensure this line is present


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
def description_list(request):
    descriptions = Description.objects.all()
    perfumes = Perfume.objects.all()  # Assurez-vous d'obtenir tous les parfums
    return render(request, 'description.html', {'descriptions': descriptions, 'perfumes': perfumes})