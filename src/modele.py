"""Entraînement, évaluation et prédiction du prix des maisons."""

import os
import json
import joblib
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error

from donnees import COLONNES_NUMERIQUES, COLONNES_CATEGORIELLES
from exceptions import DonneeInvalideError

class Modele:
    """Modèle permettant de prédire le prix des maisons."""

    def __init__(self):
        self._pipeline = None
        self._resultats = {} 
      
    def creer_pipeline(self):
      
        """Prépare les données et crée le modèle."""

        numerique = SimpleImputer(strategy="median")

        categoriel = Pipeline([
            ("imputation", SimpleImputer(strategy="most_frequent")),
            ("encodage", OneHotEncoder(handle_unknown="ignore"))
        ])

        preparation = ColumnTransformer([
            ("num", numerique, COLONNES_NUMERIQUES),
            ("cat", categoriel, COLONNES_CATEGORIELLES)
        ])

        self._pipeline = Pipeline([
            ("preparation", preparation),
            ("regression", LinearRegression())
        ])

    def entrainer(self, X_train, y_train) -> None:
        """Entraîne le modèle avec les données d'entraînement."""

        if X_train.empty or y_train.empty:
            raise DonneeInvalideError(
                "Les données d'entraînement sont vides."
            )

        self.creer_pipeline()

        self._pipeline.fit(X_train, y_train)

    @staticmethod
    def calculer_rmse(reels, predictions) -> float:
        """Calcule l'erreur RMSE avec NumPy."""

        reels = np.asarray(reels, dtype=float)
        predictions = np.asarray(predictions, dtype=float)

        if reels.size == 0 or reels.shape != predictions.shape:
            raise DonneeInvalideError(
                "Données invalides pour calculer le RMSE."
            )

        return float(
            np.sqrt(np.mean((reels - predictions) ** 2))
        )

    def evaluer(self, X_train, y_train, X_test, y_test) -> dict:
        """Évalue le modèle et le compare à une référence."""

        if self._pipeline is None:
            raise DonneeInvalideError(
                "Le modèle n'est pas entraîné."
            )

        if X_test.empty or y_test.empty:
            raise DonneeInvalideError(
                "Les données de test sont vides."
            )

        # Prédictions du modèle
        predictions = self._pipeline.predict(X_test)

        # Référence : toujours prédire le prix moyen
        moyenne = float(np.mean(y_train))
        reference = np.full(len(y_test), moyenne)

        # Calculer les erreurs
        rmse_modele = self.calculer_rmse(y_test, predictions)
        rmse_reference = self.calculer_rmse(y_test, reference)

        self._resultats = {
            "rmse_modele": rmse_modele,
            "rmse_reference": rmse_reference
        }

        return self._resultats

    def predire(self, caracteristiques) -> float:
        """Prédit le prix d'une maison."""

        if self._pipeline is None:
            raise DonneeInvalideError(
                "Le modèle n'est pas entraîné."
            )

        resultat = self._pipeline.predict(caracteristiques)

        return float(resultat[0])

    def sauvegarder(self, chemin: str, metadata: dict) -> None:
        """Sauvegarde le modèle et ses métadonnées."""

        if self._pipeline is None:
            raise DonneeInvalideError(
                "Aucun modèle à sauvegarder."
            )

        dossier = os.path.dirname(chemin)

        if dossier:
            os.makedirs(dossier, exist_ok=True)

        # Sauvegarder le modèle entraîné
        joblib.dump(self._pipeline, chemin)

        # Créer le chemin du fichier JSON
        chemin_json = os.path.splitext(chemin)[0] + ".json"

        # Sauvegarder les métadonnées
        with open(chemin_json, "w", encoding="utf-8") as fichier:
            json.dump(metadata, fichier, indent=4, ensure_ascii=False)

    def charger(self, chemin: str) -> None:
        """Charge un modèle déjà entraîné."""

        if not os.path.isfile(chemin):
            raise DonneeInvalideError(
                f"Modèle introuvable : {chemin}"
            )

        self._pipeline = joblib.load(chemin)

    def __repr__(self) -> str:
        """Retourne une représentation du modèle."""

        if self._pipeline is None:
            etat = "non chargé"
        else:
            etat = "chargé"

        return f"Modele({etat})"

