import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import re

class FragranceAI:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load_data()
        self.model = None
        self.mlb = MultiLabelBinarizer()
        self.train_model()

    def load_data(self):
        """Load and prepare the data for the AI."""
        try:
            data = pd.read_csv(self.filepath, encoding='ISO-8859-1')
            data.columns = data.columns.str.strip()  # Remove whitespace from column names
            print(f"Data loaded successfully: {data.shape[0]} rows, {data.shape[1]} columns")
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()

    def create_training_data(self):
        """Create training data for the model."""
        if 'Notes' in self.data.columns:
            self.data['Notes'] = self.data['Notes'].fillna('')
            notes_data = self.data['Notes'].str.split(',').apply(lambda x: [note.strip() for note in x if note.strip()])
            combinations = notes_data.apply(lambda notes: list(itertools.combinations(notes, 3)))
            training_data = combinations.explode().dropna().tolist()
            return training_data
        else:
            print("The 'Notes' column does not exist in the DataFrame.")
            return []

    def train_model(self):
        """Train the AI model for note combination recommendations."""
        combinations = self.create_training_data()
        if combinations:
            X = self.mlb.fit_transform(combinations)
            y = [1] * len(X)  # Dummy target variable
            X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model = KNeighborsClassifier(n_neighbors=5)
            self.model.fit(X_train, y_train)
            print("AI model trained successfully.")
        else:
            print("No training data available.")

    def clean_text(self, text):
        """Clean the text from special characters, HTML tags, and unwanted phrases."""
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'[\x80-\xFF]+', '', text)
        unwanted_phrases = [
            "Click Here For Ingredients", 
            "Close", 
            "Please be aware that ingredient lists may change or vary from time to time.", 
            "Please refer to the ingredient list on the product package you receive for the most up to date list of ingredients."
        ]
        for phrase in unwanted_phrases:
            text = text.replace(phrase, "")
        return text.strip()

    def get_suggestions(self, fragrance_choice, limit=50):
        """Predict note combinations based on the chosen fragrance."""
        if self.model:
            if fragrance_choice not in self.mlb.classes_:
                print(f"The note '{fragrance_choice}' does not exist in the available data.")
                return []
            fragrance_choice_encoded = self.mlb.transform([[fragrance_choice]])
            distances, indices = self.model.kneighbors(fragrance_choice_encoded, n_neighbors=limit)
            suggestions = []
            for idx in indices[0]:
                combination_array = np.array([self.model._fit_X[idx]])
                combination = self.mlb.inverse_transform(combination_array)[0]
                filtered_combination = [note for note in combination if note != fragrance_choice]
                if len(filtered_combination) >= 2:
                    suggested_combination = f"{fragrance_choice} + {filtered_combination[0]} + {filtered_combination[1]}"
                    clean_suggestion = self.clean_text(suggested_combination)
                    suggestions.append(clean_suggestion)
            return suggestions[:limit]
        else:
            print("The model is not trained.")
            return []

    def find_existing_perfumes(self, suggested_combinations, limit=5):
        """Find existing perfumes based on the suggested combinations."""
        found_perfumes = []
        for combination in suggested_combinations:
            notes = combination.split(' + ')
            matching_perfumes = self.data[self.data['Notes'].apply(lambda x: all(note.strip() in x for note in notes))]
            found_perfumes.extend(matching_perfumes.head(limit).to_dict(orient='records'))
        print("Found perfumes:", found_perfumes)  # Debugging line
        return found_perfumes[:limit]

# Example usage
if __name__ == "__main__":
    filepath = "D:\\5TWIN\\projet_django\\commande_perso\\final_perfume_data.csv"
    fragrance_ai = FragranceAI(filepath)

    # Test the suggestion function
    suggestions = fragrance_ai.get_suggestions("tangerine")
    print("AI Suggestions:", suggestions)

    # Find and display existing perfumes based on the suggestions
    existing_perfumes = fragrance_ai.find_existing_perfumes(suggestions, limit=5)
    for perfume in existing_perfumes:
        print(f"Name: {perfume['Nom']}")
        print(f"Description: {perfume['Description']}")
        if perfume['Image']:
            print(f"Image: {perfume['Image']}")
        print("\n")
