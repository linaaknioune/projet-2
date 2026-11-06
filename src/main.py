"""Point d'entrée : prépare les données et le modèle, puis ouvre l'interface."""
import os
import sys
 
from donnees import JeuDeDonnees, decrire_variables, separer
from exceptions import DonneeInvalideError
from interface import lancer
from modele import Modele
 
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(RACINE, "donnees", "train.csv")
CHEMIN_MODELE = os.path.join(RACINE, "Modeles", "modele.joblib")
 
 
def main() -> None:
    jeu = JeuDeDonnees(CSV).charger()
    jeu.nettoyer()
    X_train, X_test, y_train, y_test = separer(jeu.df)
 
    modele = Modele()
    nouveau = not os.path.isfile(CHEMIN_MODELE)
    if nouveau:
        modele.entrainer(X_train, y_train)
    else:
        modele.charger(CHEMIN_MODELE)
    resultats = modele.evaluer(X_train, y_train, X_test, y_test)
    if nouveau:
        modele.sauvegarder(CHEMIN_MODELE, resultats)
 
    lancer(modele, decrire_variables(X_train), resultats["rmse_modele"])
 
 
if __name__ == "__main__":
    try:
        main()
    except DonneeInvalideError as erreur:
        sys.exit(f"Erreur : {erreur}")
 
