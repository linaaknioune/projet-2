"""Point d'entrée : charge (ou entraîne) le modèle, puis ouvre l'interface."""
import json
import os

from donnees import JeuDeDonnees, decrire_variables, separer
from exceptions import DonneeInvalideError
from interface import lancer
from modele import Modele

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(RACINE, "donnees", "train.csv")
CHEMIN_MODELE = os.path.join(RACINE, "Modeles", "modele.joblib")
CHEMIN_JSON = os.path.splitext(CHEMIN_MODELE)[0] + ".json"


def entrainer_et_sauvegarder() -> None:
    """Charge, nettoie, sépare, entraîne, évalue et sauvegarde le modèle."""
    print("Chargement des données...")
    jeu = JeuDeDonnees(CSV)
    jeu.charger()

    print("Nettoyage des données...")
    rapport = jeu.nettoyer()
    print("Rapport de nettoyage :", rapport)

    X_train, X_test, y_train, y_test = separer(jeu.df)
    metadata = decrire_variables(X_train)

    print("Entraînement de la régression linéaire...")
    modele = Modele()
    modele.entrainer(X_train, y_train)

    resultats = modele.evaluer(X_train, y_train, X_test, y_test)
    print("Résultats :", resultats)

    modele.sauvegarder(CHEMIN_MODELE, {
        "algorithme": "Régression linéaire",
        "cible": "SalePrice",
        "variables": metadata,
        "evaluation": resultats,
    })
    print("Modèle sauvegardé.")


def charger_metadonnees() -> dict:
    """Lit les variables décrites dans le JSON sauvegardé avec le modèle."""
    if not os.path.isfile(CHEMIN_JSON):
        raise DonneeInvalideError(f"Métadonnées introuvables : {CHEMIN_JSON}")
    try:
        with open(CHEMIN_JSON, encoding="utf-8") as fichier:
            return json.load(fichier)["variables"]
    except (json.JSONDecodeError, KeyError) as erreur:
        raise DonneeInvalideError(f"Métadonnées illisibles : {erreur!r}") from None


def main() -> None:
    """Entraîne seulement si aucun modèle n'est sauvegardé, puis lance l'interface."""
    try:
        if not (os.path.isfile(CHEMIN_MODELE) and os.path.isfile(CHEMIN_JSON)):
            entrainer_et_sauvegarder()
        modele = Modele()
        modele.charger(CHEMIN_MODELE)
        metadata = charger_metadonnees()
    except DonneeInvalideError as erreur:
        print(f"Erreur dans les données ou le modèle : {erreur}")
        return
    lancer(modele, metadata)


if __name__ == "__main__":
    main()
