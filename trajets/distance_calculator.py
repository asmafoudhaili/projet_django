import pandas as pd
import numpy as np

# Constants
R = 6371  # Earth radius in kilometers

# Functions
def deg_to_rad(degrees):
    return degrees * (np.pi / 180)

def dist(lat1, lon1, lat2, lon2):
    d_lat = deg_to_rad(lat2 - lat1)
    d_lon = deg_to_rad(lon2 - lon1)
    a = np.sin(d_lat / 2)**2 + np.cos(deg_to_rad(lat1)) * np.cos(deg_to_rad(lat2)) * np.sin(d_lon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

# Create a DataFrame for the governorates with their coordinates
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

# Create a dictionary to hold the coordinates for easier access
coords_dict = {row['Governorate']: (row['Latitude'], row['Longitude']) for index, row in governorates_df.iterrows()}

def calculate_distances(arrival_latitude, arrival_longitude):
    distances = {}
    for governorate, (lat, lon) in coords_dict.items():
        distances[governorate] = dist(arrival_latitude, arrival_longitude, lat, lon)
    return distances

def find_closest_departure(arrival_latitude, arrival_longitude):
    distances = calculate_distances(arrival_latitude, arrival_longitude)
    closest_departure = min(distances, key=distances.get)
    return closest_departure

# Example usage
arrival_point_latitude = 34.5000  # Example latitude
arrival_point_longitude = 9.5000   # Example longitude
closest_departure_point = find_closest_departure(arrival_point_latitude, arrival_point_longitude)
print(f"The closest departure point is: {closest_departure_point}")
