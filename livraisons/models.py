from django.db import models

class Livraison(models.Model):
    # Define the governorates data with coordinates as a class variable
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

    # Create a dictionary to hold the coordinates as a class variable
    coords_dict = {governorate: (latitude, longitude) 
                   for governorate, latitude, longitude in zip(
                       governorates_data['Governorate'], 
                       governorates_data['Latitude'], 
                       governorates_data['Longitude']
                   )}

    GOUVERNORATS = [(governorate, governorate) for governorate in governorates_data['Governorate']]
    
    # Define your model fields
    commande = models.CharField(max_length=100)
    adresse_livraison = models.CharField(max_length=255, choices=GOUVERNORATS)
    statut_livraison = models.CharField(max_length=50)
    transporteur = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.commande} - {self.statut_livraison}"

    def get_lat_long(self):
        # Retrieve latitude and longitude based on the governorate
        return self.coords_dict.get(self.adresse_livraison, None)
