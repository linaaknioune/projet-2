import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from donnees import COLONNES_NUMERIQUES, COLONNES_CATEGORIELLES
from exceptions import DonneeInvalideError
from modele import Modele


@pytest.fixture
def donnees_exemple():
    n = 12
    X = pd.DataFrame({
        'OverallQual': [4, 5, 6, 7] * 3,
        'GrLivArea': [900, 1100, 1400, 1800] * 3,
        'TotalBsmtSF': [500, 600, 800, 900] * 3,
        'GarageCars': [1, 1, 2, 2] * 3,
        'YearBuilt': [1980, 1990, 2000, 2010] * 3,
        'FullBath': [1, 1, 2, 2] * 3,
        'LotArea': [5000, 6000, 7000, 8000] * 3,
        'Neighborhood': ['NAmes', 'CollgCr', 'NAmes', 'CollgCr'] * 3,
        'KitchenQual': ['TA', 'Gd', 'TA', 'Gd'] * 3,
        'CentralAir': ['Y', 'Y', 'N', 'Y'] * 3,
    })
    y = pd.Series([100000, 140000, 190000, 240000] * 3, dtype=float)
    return X, y


@pytest.fixture
def modele_entraine(donnees_exemple):
    X, y = donnees_exemple
    modele = Modele()
    modele.entrainer(X, y)
    return modele


def test_initialisation():
    modele = Modele()
    assert modele._pipeline is None
    assert modele._resultats == {}


def test_creer_pipeline():
    modele = Modele()
    modele.creer_pipeline()
    assert isinstance(modele._pipeline, Pipeline)
    assert isinstance(modele._pipeline.named_steps['preparation'], ColumnTransformer)
    assert isinstance(modele._pipeline.named_steps['regression'], LinearRegression)
    preparation = modele._pipeline.named_steps['preparation']
    assert list(preparation.transformers[0][2]) == COLONNES_NUMERIQUES
    assert list(preparation.transformers[1][2]) == COLONNES_CATEGORIELLES


def test_entrainer(donnees_exemple):
    X, y = donnees_exemple
    modele = Modele()
    modele.entrainer(X, y)
    assert modele._pipeline is not None
    assert np.isfinite(modele._pipeline.predict(X)).all()


@pytest.mark.parametrize('vide', ['X', 'y'])
def test_entrainer_donnees_vides(donnees_exemple, vide):
    X, y = donnees_exemple
    if vide == 'X':
        X = X.iloc[:0]
    else:
        y = y.iloc[:0]
    with pytest.raises(DonneeInvalideError, match='vides'):
        Modele().entrainer(X, y)


def test_entrainer_valeurs_manquantes(donnees_exemple):
    X, y = donnees_exemple
    X = X.copy()
    X.loc[0, 'GrLivArea'] = np.nan
    X.loc[1, 'KitchenQual'] = None
    modele = Modele()
    modele.entrainer(X, y)
    assert np.isfinite(modele.predire(X.iloc[[0]]))


def test_predire_categorie_inconnue(modele_entraine, donnees_exemple):
    X, _ = donnees_exemple
    nouveau = X.iloc[[0]].copy()
    nouveau.loc[nouveau.index[0], 'Neighborhood'] = 'QuartierInconnu'
    assert np.isfinite(modele_entraine.predire(nouveau))


def test_calculer_rmse_zero():
    assert Modele.calculer_rmse([10, 20], [10, 20]) == pytest.approx(0)


def test_calculer_rmse_valeur_connue():
    assert Modele.calculer_rmse([3, 5], [0, 1]) == pytest.approx(np.sqrt(12.5))


@pytest.mark.parametrize('reels,predictions', [([], []), ([1, 2], [1]), ([1, 2], [[1, 2]])])
def test_calculer_rmse_donnees_invalides(reels, predictions):
    with pytest.raises(DonneeInvalideError):
        Modele.calculer_rmse(reels, predictions)


def test_evaluer(modele_entraine, donnees_exemple):
    X, y = donnees_exemple
    resultats = modele_entraine.evaluer(X, y, X, y)
    assert set(resultats) == {'rmse_modele', 'rmse_reference'}
    assert all(np.isfinite(v) and v >= 0 for v in resultats.values())
    assert resultats['rmse_modele'] <= resultats['rmse_reference']
    assert modele_entraine._resultats == resultats


def test_evaluer_avant_entrainement(donnees_exemple):
    X, y = donnees_exemple
    with pytest.raises(DonneeInvalideError, match='pas entraîné'):
        Modele().evaluer(X, y, X, y)


@pytest.mark.parametrize('vide', ['X', 'y'])
def test_evaluer_test_vide(modele_entraine, donnees_exemple, vide):
    X, y = donnees_exemple
    X_test = X.iloc[:0] if vide == 'X' else X
    y_test = y.iloc[:0] if vide == 'y' else y
    with pytest.raises(DonneeInvalideError, match='vides'):
        modele_entraine.evaluer(X, y, X_test, y_test)


def test_predire(modele_entraine, donnees_exemple):
    X, _ = donnees_exemple
    prediction = modele_entraine.predire(X.iloc[[0]])
    assert isinstance(prediction, float)
    assert np.isfinite(prediction)


def test_predire_avant_entrainement(donnees_exemple):
    X, _ = donnees_exemple
    with pytest.raises(DonneeInvalideError, match='pas entraîné'):
        Modele().predire(X.iloc[[0]])


def test_sauvegarder(modele_entraine, tmp_path):
    chemin = tmp_path / 'sous_dossier' / 'modele.joblib'
    metadata = {'nom': 'regression', 'version': 1}
    modele_entraine.sauvegarder(str(chemin), metadata)
    assert chemin.is_file()
    assert chemin.with_suffix('.json').is_file()
    assert json.loads(chemin.with_suffix('.json').read_text(encoding='utf-8')) == metadata
    assert isinstance(joblib.load(chemin), Pipeline)


def test_sauvegarder_avant_entrainement(tmp_path):
    with pytest.raises(DonneeInvalideError, match='Aucun modèle'):
        Modele().sauvegarder(str(tmp_path / 'modele.joblib'), {})


def test_charger_et_predire(modele_entraine, donnees_exemple, tmp_path):
    X, _ = donnees_exemple
    chemin = tmp_path / 'modele.joblib'
    modele_entraine.sauvegarder(str(chemin), {'test': True})
    autre = Modele()
    autre.charger(str(chemin))
    assert autre.predire(X.iloc[[0]]) == pytest.approx(modele_entraine.predire(X.iloc[[0]]))


def test_charger_fichier_absent(tmp_path):
    with pytest.raises(DonneeInvalideError, match='introuvable'):
        Modele().charger(str(tmp_path / 'absent.joblib'))


def test_repr(modele_entraine):
    assert repr(Modele()) == 'Modele(non chargé)'
    assert repr(modele_entraine) == 'Modele(chargé)'


