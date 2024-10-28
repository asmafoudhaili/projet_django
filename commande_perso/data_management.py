import pandas as pd
import itertools

class FragranceDataManagement:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load_data()
        self.combinations_df = None
        self.create_note_combinations()

    def load_data(self):
        """Charger les données à partir du fichier CSV."""
        try:
            # Essayez avec un encodage alternatif comme ISO-8859-1 ou Windows-1252
            data = pd.read_csv(self.filepath, encoding='ISO-8859-1')  # Remplacez par 'windows-1252' si nécessaire
            print(f"Données chargées : {len(data)} lignes.")

            # Nettoyer les noms de colonnes pour enlever les espaces
            data.columns = data.columns.str.strip()
            print("Colonnes dans le DataFrame :", data.columns.tolist())  # Affiche les colonnes
            return data
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")
            return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur

    def create_note_combinations(self):
        """Créer toutes les combinaisons possibles de notes."""
        if 'Notes' in self.data.columns:
            # Extraire et nettoyer les notes
            unique_notes = self.data['Notes'].str.cat(sep=',').split(',')
            unique_notes = [note.strip() for note in set(unique_notes) if note.strip() and "Click Here" not in note]

            # Créer toutes les combinaisons possibles de notes
            self.combinations_df = pd.DataFrame(
                list(itertools.combinations(unique_notes, 2)),
                columns=['Note_1', 'Note_2']
            )
            print(f"Combinaisons de notes créées : {len(self.combinations_df)}")
        else:
            print("La colonne 'Notes' n'existe pas dans le DataFrame.")

    def get_suggestions(self, fragrance_choice, limit=50):
        """Obtenir les combinaisons de notes pour la note choisie, limité à un nombre défini de suggestions."""
        if self.combinations_df is not None:
            print(f"Recherche de combinaisons pour : {fragrance_choice}")
            
            # Chercher la note choisie dans toutes les combinaisons
            combinations = self.combinations_df[
                (self.combinations_df['Note_1'] == fragrance_choice) | (self.combinations_df['Note_2'] == fragrance_choice)
            ]

            if combinations.empty:
                print(f"Aucune combinaison trouvée pour {fragrance_choice}.")
                return []

            # Limiter les suggestions selon le paramètre `limit` et éliminer les doublons
            limited_combinations = combinations.apply(lambda x: f"{x['Note_1']} + {x['Note_2']}", axis=1).unique()[:limit].tolist()
            return limited_combinations

        return []

# Exemple d'utilisation (peut être commenté dans le fichier final)
if __name__ == "__main__":
    filepath = "D:\\5TWIN\\projet_django\\commande_perso\\final_perfume_data.csv"  # Remplacez par le chemin vers votre fichier CSV
    fragrance_manager = FragranceDataManagement(filepath)

    # Tester la fonction de suggestion
    suggestions = fragrance_manager.get_suggestions("Berries")
    print("Suggestions :", suggestions)
