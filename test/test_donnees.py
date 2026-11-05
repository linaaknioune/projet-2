import pandas as pd
import pytest
from donnees import (COLONNES_CATEGORIELLES, COLONNES_NUMERIQUES, JeuDeDonnees,
                     decrire_variables, separer)
from exceptions import DonneeInvalideError

def test_charger_fichier_valide(csv_synthetique):
    jeu = JeuDeDonnees(csv_synthetique).charger()
    assert len(jeu) == 300
def test_charger_fichier_introuvable(tmp_path):
    with pytest.raises(DonneeInvalideError):
        JeuDeDonnees(str(tmp_path / "absent.csv")).charger()
def test_charger_colonne_manquante(tmp_path, df_synthetique):
    chemin = tmp_path / "incomplet.csv"
    df_synthetique.drop(columns=["GrLivArea"]).to_csv(chemin, index=False)
    with pytest.raises(DonneeInvalideError, match="GrLivArea"):
        JeuDeDonnees(str(chemin)).charger()
def test_acces_avant_chargement():
    with pytest.raises(DonneeInvalideError):
        JeuDeDonnees("x.csv").df
def test_nettoyer_retire_les_lignes_invalides(csv_synthetique):
    jeu = JeuDeDonnees(csv_synthetique).charger()
    df = jeu.df.copy()
    df.loc[0, "SalePrice"] = None     
    df.loc[1, "SalePrice"] = -5       
    df.loc[2, "GrLivArea"] = 5000     
    jeu._df = df
    rapport = jeu.nettoyer()
    assert rapport["cible_invalide"] == 2
    assert rapport["surface_aberrante"] == 1
    assert len(jeu) == 297
def test_nettoyer_garde_une_valeur_manquante_de_caracteristique(csv_synthetique):
    jeu = JeuDeDonnees(csv_synthetique).charger()
    jeu._df.loc[3, "TotalBsmtSF"] = None
    jeu.nettoyer()
    assert jeu.df["TotalBsmtSF"].isna().sum() == 1   
def test_separer_proportions_et_reproductibilite(df_synthetique):
    a = separer(df_synthetique, taille_test=0.2, graine=1)
    b = separer(df_synthetique, taille_test=0.2, graine=1)
    assert len(a[1]) == pytest.approx(60, abs=1)
    assert list(a[1].index) == list(b[1].index)      
    assert set(a[0].index).isdisjoint(a[1].index)     
@pytest.mark.parametrize("taille", [0, 1, -0.5, 1.5])
def test_separer_taille_invalide(df_synthetique, taille):
    with pytest.raises(DonneeInvalideError):
        separer(df_synthetique, taille_test=taille)
def test_decrire_variables(df_synthetique):
    X = df_synthetique[COLONNES_NUMERIQUES + COLONNES_CATEGORIELLES]
    desc = decrire_variables(X)
    assert desc["numeriques"]["OverallQual"]["type"] == "int"
    assert desc["numeriques"]["OverallQual"]["min"] == X["OverallQual"].min()
    assert desc["categorielles"]["CentralAir"] == ["N", "Y"]
