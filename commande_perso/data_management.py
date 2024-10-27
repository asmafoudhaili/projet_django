import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
from imblearn.over_sampling import SMOTE
import numpy as np

class PerfumeDataManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.encoder = OneHotEncoder(sparse_output=True, handle_unknown='ignore')
        self.combinations_df = None

    def load_data(self):
        """Charger les données depuis un fichier CSV."""
        self.data = pd.read_csv(self.file_path, encoding='ISO-8859-1')
        print("Données chargées avec succès.")

    def clean_data(self):
        """Nettoyer les données."""
        self.data.dropna(subset=['Notes'], inplace=True)
        print("Données nettoyées.")

    def transform_data(self):
        """Transformer les données avec OneHotEncoder."""
        notes_reshaped = np.array(self.data['Notes'].tolist()).reshape(-1, 1)
        encoded_notes = self.encoder.fit_transform(notes_reshaped)
        self.encoded_notes_df = pd.DataFrame(encoded_notes.toarray(), columns=self.encoder.get_feature_names_out())
        print("Données transformées.")

    def create_note_combinations(self):
        """Créer des combinaisons de notes."""
        unique_notes = self.data['Notes'].str.cat(sep=',').split(',')
        unique_notes = [note.strip() for note in set(unique_notes)]
        unique_notes = unique_notes[:100]  # Garder uniquement les 100 premières notes uniques
        self.combinations_df = pd.DataFrame([(note1, note2) for i, note1 in enumerate(unique_notes) for note2 in unique_notes[i + 1:]], columns=['Note_1', 'Note_2'])
        print(f"Combinaisons de notes créées : {len(self.combinations_df)}")

    def prepare_data(self):
        """Préparer les données pour l'entraînement du modèle."""
        if self.combinations_df is not None:
            # Encoder les combinaisons de notes
            encoded_combinations = self.encoder.fit_transform(self.combinations_df[['Note_1', 'Note_2']])
            self.combinations_df_encoded = pd.DataFrame(encoded_combinations.toarray(), columns=self.encoder.get_feature_names_out())
            self.combinations_df_encoded['Label'] = 1  # Étiquette 1 pour les combinaisons existantes

            # Création d’échantillons négatifs
            negative_samples = self._create_negative_samples()
            negative_encoded = self.encoder.transform(negative_samples)
            negative_df = pd.DataFrame(negative_encoded.toarray(), columns=self.encoder.get_feature_names_out())
            negative_df['Label'] = 0  # Étiquette 0 pour les échantillons négatifs

            # Combinaison des échantillons positifs et négatifs
            self.final_dataset = pd.concat([self.combinations_df_encoded, negative_df], ignore_index=True)

            # Division des données en ensembles d'entraînement et de test
            self.X = self.final_dataset.drop('Label', axis=1)
            self.y = self.final_dataset['Label']
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

            # Équilibrage des classes avec SMOTE
            smote = SMOTE()
            self.X_train, self.y_train = smote.fit_resample(self.X_train, self.y_train)
            print("Données préparées pour l'entraînement du modèle avec équilibrage des classes.")

    def _create_negative_samples(self):
        """Créer des échantillons négatifs de combinaisons de notes."""
        unique_notes = self.data['Notes'].str.cat(sep=',').split(',')
        unique_notes = [note.strip() for note in set(unique_notes)]
        
        negative_samples = []
        for _ in range(len(self.combinations_df) * 2):
            note_1 = np.random.choice(unique_notes)
            note_2 = np.random.choice(unique_notes)
            if note_1 != note_2:
                negative_samples.append((note_1, note_2))
        
        return negative_samples

    def train_model(self):
        """Entraîner le modèle de classification avec une recherche d'hyperparamètres."""
        # Recherche de meilleurs hyperparamètres avec GridSearchCV
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5, 10]
        }
        rf = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, scoring='recall', n_jobs=-1)
        grid_search.fit(self.X_train, self.y_train)

        self.model = grid_search.best_estimator_
        print("Modèle entraîné avec les meilleurs hyperparamètres :", grid_search.best_params_)

    def evaluate_model(self):
        """Évaluer le modèle sur les données de test."""
        predictions = self.model.predict(self.X_test)

        # Évaluation des métriques
        accuracy = accuracy_score(self.y_test, predictions)
        report = classification_report(self.y_test, predictions)

        print(f"Accuracy: {accuracy}")
        print("Classification Report:")
        print(report)

        # Matrice de confusion
        cm = confusion_matrix(self.y_test, predictions)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap=plt.cm.Blues)
        plt.title("Matrice de Confusion")
        plt.show()

        # Courbe ROC
        fpr, tpr, thresholds = roc_curve(self.y_test, predictions)
        roc_auc = auc(fpr, tpr)

        plt.figure()
        plt.plot(fpr, tpr, color='blue', lw=2, label='AUC = %0.2f' % roc_auc)
        plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Taux de Faux Positifs')
        plt.ylabel('Taux de Vrais Positifs')
        plt.title('Courbe ROC')
        plt.legend(loc='lower right')
        plt.show()

    def analyze_notes(self):
        """Analyser les notes olfactives."""
        stats = self.data['Notes'].describe(include='all')
        print(stats)

    def plot_notes_distribution(self, min_occurrences=10):
        """Visualiser la distribution des notes olfactives."""
        if self.data is not None:
            all_notes = []
            for note in self.data['Notes']:
                separated_notes = [n.strip() for n in note.split(',')]
                all_notes.extend(separated_notes)

            note_counts = pd.Series(all_notes).value_counts()
            filtered_notes = note_counts[note_counts > min_occurrences]

            plt.figure(figsize=(12, 8))
            sns.barplot(y=filtered_notes.index, x=filtered_notes.values, palette='viridis')
            plt.title("Distribution des Notes Olfactives")
            plt.xlabel("Nombre d'Occurrences")
            plt.ylabel("Notes Olfactives")
            plt.show()


if __name__ == "__main__":
    manager = PerfumeDataManager('D:\\5TWIN\\projet_django\\commande_perso\\final_perfume_data.csv')
    manager.load_data()  # Charger les données
    manager.clean_data()  # Nettoyer les données
    manager.transform_data()  # Transformer les données
    manager.create_note_combinations()  # Créer des combinaisons de notes
    manager.analyze_notes()  # Analyser les notes olfactives
    manager.prepare_data()  # Préparer les données pour l'entraînement
    manager.train_model()  # Entraîner le modèle
    manager.evaluate_model()  # Évaluer le modèle
    manager.plot_notes_distribution()  # Afficher la distribution des notes olfactives
