from django.shortcuts import render, get_object_or_404, redirect
from .models import TrajetLivraison
from .forms import TrajetLivraisonForm
import pandas as pd
import numpy as np

# Constants
R = 6371  # Earth radius in kilometers

# Your governorates data
governorates_data = {
    'Governorate': [
        'Ariana', 'Béja', 'Ben Arous', 'Bizerte', 'El Kef', 'Gabès', 'Gafsa', 'Jendouba', 
        'Kairouan', 'Kasserine', 'Kebili', 'Mahdia', 'Manouba', 'Medenine', 'Monastir', 
        'Nabeul', 'Sfax', 'Sidi Bouzid', 'Siliana', 'Sousse', 'Tataouine', 'Tozeur', 
        'Tunis', 'Zaghouan'
    ],
    'Latitude': [
        36.8625, 36.7333, 36.7108, 37.2728, 36.1917, 33.8833, 34.4225, 35.1600,
        35.6772, 35.1667, 33.7050, 35.5000, 36.7933, 33.3547, 35.7694, 
        36.4513, 34.7400, 35.0381, 35.5800, 35.8333, 32.9306, 33.6833, 
        36.8064, 36.4267
    ],
    'Longitude': [
        10.1956, 9.1833, 10.7817, 9.8725, 8.8236, 10.1167, 8.7842, 8.9981,
        10.1008, 8.8333, 8.9650, 10.3000, 10.1622, 10.5053, 10.8194, 
        10.6933, 10.7600, 9.4858, 9.1961, 10.6333, 10.4500, 8.1481, 
        10.1817, 10.1767
    ]
}

# Check lengths
lengths = {key: len(value) for key, value in governorates_data.items()}
print(lengths)

governorates_df = pd.DataFrame(governorates_data)

# Create a dictionary to hold the coordinates
coords_dict = {row['Governorate']: (row['Latitude'], row['Longitude']) for index, row in governorates_df.iterrows()}

def deg_to_rad(degrees):
    return degrees * (np.pi / 180)

def dist(lat1, lon1, lat2, lon2):
    d_lat = deg_to_rad(lat2 - lat1)
    d_lon = deg_to_rad(lon2 - lon1)
    a = np.sin(d_lat / 2)**2 + np.cos(deg_to_rad(lat1)) * np.cos(deg_to_rad(lat2)) * np.sin(d_lon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def calculate_distances(arrival_latitude, arrival_longitude):
    distances = {}
    for governorate, (lat, lon) in coords_dict.items():
        distances[governorate] = dist(arrival_latitude, arrival_longitude, lat, lon)
    return distances

def find_closest_departure(arrival_latitude, arrival_longitude):
    distances = calculate_distances(arrival_latitude, arrival_longitude)
    closest_departure = min(distances, key=distances.get)
    return closest_departure

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

def trajet_view(request):
    if request.method == 'POST':
        arrival_point_latitude = float(request.POST.get('arrival_latitude'))
        arrival_point_longitude = float(request.POST.get('arrival_longitude'))
        closest_departure_point = find_closest_departure(arrival_point_latitude, arrival_point_longitude)

        # You can return this data to the template context
        return render(request, 'trajets/result.html', {'closest_departure': closest_departure_point})

    return render(request, 'trajets/trajet_form.html')
