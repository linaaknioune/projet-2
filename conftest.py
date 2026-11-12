import sys
import pytest
import pandas as pd
import numpy as np
from pathlib import Path


# Ajouter le dossier src au début du chemin de recherche
RACINE = Path(__file__).resolve().parent
SRC = RACINE / "src"

sys.path.insert(0, str(SRC))

@pytest.fixture
def df_synthetique() -> pd.DataFrame:
    """300 maisons fictives (utilisées par test_donnees.py)."""
    rng = np.random.default_rng(0)
    n = 300
    surface = rng.uniform(600, 3000, n).round(1)
    qualite = rng.integers(3, 10, n)
    df = pd.DataFrame({
        "OverallQual": qualite,
        "GrLivArea": surface,
        "TotalBsmtSF": rng.uniform(0, 1500, n).round(1),
        "GarageCars": rng.integers(0, 4, n),
        "YearBuilt": rng.integers(1900, 2010, n),
        "FullBath": rng.integers(1, 4, n),
        "LotArea": rng.integers(3000, 20000, n),
        "Neighborhood": rng.choice(["NAmes", "CollgCr", "OldTown", "Edwards"], n),
        "KitchenQual": rng.choice(["Ex", "Gd", "TA", "Fa"], n),
        "CentralAir": ["Y", "N"] * (n // 2),
    })
    df["SalePrice"] = (20000 * qualite + 60 * surface + rng.normal(0, 5000, n)).round(0)
    return df


@pytest.fixture
def csv_synthetique(tmp_path, df_synthetique) -> str:
    """Écrit le jeu synthétique dans un CSV temporaire et retourne son chemin."""
    chemin = tmp_path / "synthetique.csv"
    df_synthetique.to_csv(chemin, index=False)
    return str(chemin)

