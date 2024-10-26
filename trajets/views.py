from django.shortcuts import render, get_object_or_404, redirect
from .models import TrajetLivraison
from .forms import TrajetLivraisonForm

def trajet_list(request):
    trajets = TrajetLivraison.objects.all()
    return render(request, 'trajets/trajet_list.html', {'trajets': trajets})

def trajet_detail(request, pk):
    trajet = get_object_or_404(TrajetLivraison, pk=pk)
    return render(request, 'trajets/trajet_detail.html', {'trajet': trajet})

def trajet_create(request):
    if request.method == 'POST':
        form = TrajetLivraisonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trajet_list')
    else:
        form = TrajetLivraisonForm()
    return render(request, 'trajets/trajet_form.html', {'form': form})

def trajet_update(request, pk):
    trajet = get_object_or_404(TrajetLivraison, pk=pk)
    if request.method == 'POST':
        form = TrajetLivraisonForm(request.POST, instance=trajet)
        if form.is_valid():
            form.save()
            return redirect('trajet_list')
    else:
        form = TrajetLivraisonForm(instance=trajet)
    return render(request, 'trajets/trajet_form.html', {'form': form})

def trajet_delete(request, pk):
    trajet = get_object_or_404(TrajetLivraison, pk=pk)
    if request.method == 'POST':
        trajet.delete()
        return redirect('trajet_list')
    return render(request, 'trajets/trajet_confirm_delete.html', {'trajet': trajet})
