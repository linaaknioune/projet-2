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
