import json
import os
from typing import Dict

import sklearn
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from donnees import COLONNES_CATEGORIELLES, COLONNES_NUMERIQUES, GRAINE
from exceptions import DonneeInvalideError, ModeleIndisponibleError
from outils import chronometre

# Métadonnées JSON

def ecrire_metadonnees(metadonnees: dict, chemin: str) -> None:
    """Écrit les métadonnées en JSON (UTF-8)."""
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(metadonnees, f, ensure_ascii=False, indent=2)


def lire_metadonnees(chemin: str) -> dict:
    """Lit les métadonnées JSON. Échoue si le fichier manque ou est corrompu."""
    if not os.path.exists(chemin):
        raise ModeleIndisponibleError(f"Métadonnées introuvables : {chemin}")
    with open(chemin, encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise DonneeInvalideError(f"JSON invalide dans {chemin} : {e}") from e


def version_sklearn() -> str:
    """Version de scikit-learn (le fichier joblib n'est fiable qu'avec la même)."""
    return sklearn.__version__

# Métrique calculé avec NumPy
def _valider(y_vrai, y_pred):
    """Convertit en tableaux NumPy 1D de même taille, non vides."""
    a = np.asarray(y_vrai, dtype=float).ravel()
    b = np.asarray(y_pred, dtype=float).ravel()
    if a.size == 0 or a.shape != b.shape:
        raise DonneeInvalideError("y_vrai et y_pred doivent avoir la même taille (non nulle).")
    return a, b


def rmse(y_vrai, y_pred) -> float:
    """Racine de l'erreur quadratique moyenne, dans l'unité de la cible ($)."""
    a, b = _valider(y_vrai, y_pred)
    return float(np.sqrt(np.mean((a - b) ** 2)))


def mae(y_vrai, y_pred) -> float:
    """Erreur absolue moyenne, dans l'unité de la cible ($)."""
    a, b = _valider(y_vrai, y_pred)
    return float(np.mean(np.abs(a - b)))


def r2(y_vrai, y_pred) -> float:
    """Coefficient de détermination (1 = parfait, 0 = aussi bon que la moyenne)."""
    a, b = _valider(y_vrai, y_pred)
    ss_tot = np.sum((a - a.mean()) ** 2)
    if ss_tot == 0:
        raise DonneeInvalideError("R² indéfini : la cible est constante.")
    return float(1 - np.sum((a - b) ** 2) / ss_tot)
