
"""Lecture, vérification, nettoyage et séparation du jeu de données."""

import os
from typing import Dict, List, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from exceptions import DonneeInvalideError

CIBLE = "SalePrice"

COLONNES_NUMERIQUES = [
    "OverallQual",
    "GrLivArea",
    "TotalBsmtSF",
    "GarageCars",
    "YearBuilt",
    "FullBath",
    "LotArea"
]

COLONNES_CATEGORIELLES = [
    "Neighborhood",
    "KitchenQual",
    "CentralAir"
]

SEUIL_SURFACE = 4000
GRAINE = 42


class JeuDeDonnees:
    """Jeu de données tabulaire chargé depuis le CSV."""

    def __init__(self, chemin: str) -> None:
        self._chemin = chemin
        self._df = None

    @property
    def df(self) -> pd.DataFrame:
        """Retourne le DataFrame chargé."""
        if self._df is None:
            raise DonneeInvalideError(
                "Appelez charger() avant d'utiliser les données."
            )
        return self._df

    def charger(self) -> "JeuDeDonnees":
        """Charge le CSV et vérifie les colonnes requises."""

        if not os.path.exists(self._chemin):
            raise DonneeInvalideError(
                f"Fichier introuvable : {self._chemin}"
            )

        with open(self._chemin, encoding="utf-8") as f:
            df = pd.read_csv(f)

        requises = (
            COLONNES_NUMERIQUES
            + COLONNES_CATEGORIELLES
            + [CIBLE]
        )

        manquantes = [c for c in requises if c not in df.columns]

        if manquantes:
            raise DonneeInvalideError(
                f"Colonnes manquantes : {manquantes}"
            )

        self._df = df
        return self

    def verifier_criteres(self) -> Dict[str, object]:
        """Vérifie les critères du jeu de données."""

        df = self.df
        entree = [
            c for c in df.columns
            if c not in (CIBLE, "Id")
        ]

        return {
            "lignes": len(df),
            "lignes_ok (500-50000)": 500 <= len(df) <= 50000,
            "colonnes_entree_dataset": len(entree),
            "numeriques_dataset": len(
                df[entree].select_dtypes(exclude="object").columns
            ),
            "categorielles_dataset": len(
                df[entree].select_dtypes(include="object").columns
            ),
            "colonnes_entree_retenues": (
                len(COLONNES_NUMERIQUES)
                + len(COLONNES_CATEGORIELLES)
            )
        }

    def valeurs_manquantes(self) -> pd.Series:
        """Calcule le pourcentage de valeurs manquantes."""

        cols = (
            COLONNES_NUMERIQUES
            + COLONNES_CATEGORIELLES
            + [CIBLE]
        )

        return (
            self.df[cols].isna().mean() * 100
        ).sort_values(ascending=False)

    def nettoyer(self) -> Dict[str, int]:
        """Nettoie les données."""

        cols = (
            COLONNES_NUMERIQUES
            + COLONNES_CATEGORIELLES
            + [CIBLE]
        )

        df = self.df[cols]
        rapport = {}

        n = len(df)
        df = df.drop_duplicates()
        rapport["doublons"] = n - len(df)

        n = len(df)
        df = df[df[CIBLE].notna() & (df[CIBLE] > 0)]
        rapport["cible_invalide"] = n - len(df)

        n = len(df)
        df = df[~(df["GrLivArea"] > SEUIL_SURFACE)]
        rapport["surface_aberrante"] = n - len(df)

        self._df = df.reset_index(drop=True)

        return rapport

    def __len__(self) -> int:
        return len(self.df)

    def __repr__(self) -> str:
        etat = (
            "non chargé"
            if self._df is None
            else f"{len(self._df)} lignes"
        )
        return f"JeuDeDonnees({self._chemin!r}, {etat})"


def separer(
    df: pd.DataFrame,
    taille_test: float = 0.2,
    graine: int = GRAINE
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Sépare les données en ensembles d'entraînement et de test."""

    if not 0 < taille_test < 1:
        raise DonneeInvalideError(
            "taille_test doit être entre 0 et 1 (exclus)."
        )

    X = df[COLONNES_NUMERIQUES + COLONNES_CATEGORIELLES]
    y = df[CIBLE]

    return train_test_split(
        X,
        y,
        test_size=taille_test,
        random_state=graine
    )


def decrire_variables(X_train: pd.DataFrame) -> Dict[str, dict]:
    """Décrit les variables pour construire l'interface."""

    numeriques = {}

    for col in COLONNES_NUMERIQUES:
        serie = X_train[col].dropna()

        est_entier = bool(
            (serie == serie.round()).all()
        )

        numeriques[col] = {
            "type": "int" if est_entier else "float",
            "min": float(serie.min()),
            "max": float(serie.max())
        }

    categorielles: Dict[str, List[str]] = {
        col: sorted(
            X_train[col].dropna().astype(str).unique().tolist()
        )
        for col in COLONNES_CATEGORIELLES
    }

    return {
        "numeriques": numeriques,
        "categorielles": categorielles
    }
