from django.shortcuts import render, get_object_or_404, redirect
from .models import Livraison
from .forms import LivraisonForm

def livraison_list(request):
    livraisons = Livraison.objects.all()
    return render(request, 'livraisons/livraison_list.html', {'livraisons': livraisons})

def livraison_detail(request, pk):
    livraison = get_object_or_404(Livraison, pk=pk)
    return render(request, 'livraisons/livraison_detail.html', {'livraison': livraison})

def livraison_create(request):
    if request.method == 'POST':
        form = LivraisonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('livraison_list')
    else:
        form = LivraisonForm()
    return render(request, 'livraisons/livraison_form.html', {'form': form})

def livraison_update(request, pk):
    livraison = get_object_or_404(Livraison, pk=pk)
    if request.method == 'POST':
        form = LivraisonForm(request.POST, instance=livraison)
        if form.is_valid():
            form.save()
            return redirect('livraison_list')
    else:
        form = LivraisonForm(instance=livraison)
    return render(request, 'livraisons/livraison_form.html', {'form': form})

def livraison_delete(request, pk):
    livraison = get_object_or_404(Livraison, pk=pk)
    if request.method == 'POST':
        livraison.delete()
        return redirect('livraison_list')
    return render(request, 'livraisons/livraison_confirm_delete.html', {'livraison': livraison})
