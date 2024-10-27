from django.db import models
from livraisons.models import Livraison
import numpy as np

# Constants
R = 6371  # Earth radius in kilometers

# Coordinates for Tunis and Sfax
DEPARTURE_POINTS = {
    'Tunis': (36.8064, 10.1817),
    'Sfax': (34.7400, 10.7600)
}

def deg_to_rad(degrees):
    """Convert degrees to radians."""
    return degrees * (np.pi / 180)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the Haversine distance between two points."""
    d_lat = deg_to_rad(lat2 - lat1)
    d_lon = deg_to_rad(lon2 - lon1)
    a = np.sin(d_lat / 2)**2 + np.cos(deg_to_rad(lat1)) * np.cos(deg_to_rad(lat2)) * np.sin(d_lon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def find_closest_departure(arrival_latitude, arrival_longitude):
    """Find the closest departure point (Tunis or Sfax) to the arrival location."""
    distances = {
        departure: calculate_distance(arrival_latitude, arrival_longitude, lat, lon)
        for departure, (lat, lon) in DEPARTURE_POINTS.items()
    }
    return min(distances, key=distances.get)

class TrajetLivraison(models.Model):
    livraison = models.OneToOneField(Livraison, on_delete=models.CASCADE, related_name='trajet')
    temps_estime = models.DurationField()
    point_de_depart = models.CharField(max_length=255, blank=True)
    point_d_arrivee = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        """Override save method to automatically choose the closest departure point."""
        if not self.point_d_arrivee and self.livraison:
            self.point_d_arrivee = self.livraison.adresse_livraison  # Set arrival point if not already set
            
        if self.livraison:
            arrival_latitude, arrival_longitude = self.livraison.get_lat_long()  # Retrieve coordinates of arrival
            self.point_de_depart = find_closest_departure(arrival_latitude, arrival_longitude)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Trajet for {self.livraison.commande} with estimated time {self.temps_estime} from {self.point_de_depart} to {self.point_d_arrivee}"
