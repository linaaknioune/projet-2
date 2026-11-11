"""Point d'entrée : prépare les données et le modèle, puis ouvre l'interface."""
import os

 
from donnees import JeuDeDonnees, decrire_variables, separer
from exceptions import DonneeInvalideError
from interface import lancer
from modele import Modele
 
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(RACINE, "donnees", "train.csv")
CHEMIN_MODELE = os.path.join(RACINE, "Modeles", "modele.joblib")
 
 
def main():
    """Prépare le modèle et lance l'interface."""
    try:
        # 1. Charger les données
        print("Chargement des données...")
        jeu = JeuDeDonnees(CSV)
        jeu.charger()

        # 2. Nettoyer les données
        print("Nettoyage des données...")
        rapport = jeu.nettoyer()
        print("Rapport de nettoyage :", rapport)

        # 3. Séparer les données
        print("Séparation des données...")
        X_train, X_test, y_train, y_test = separer(jeu.df)

        # 4. Décrire les variables
        metadata = decrire_variables(X_train) 

        # 5. Entraîner la régression linéaire
        print("Entraînement de la régression linéaire...")
        modele = Modele()
        modele.entrainer(X_train, y_train)

        # 6. Évaluer le modèle
        resultats = modele.evaluer(
            X_train, y_train, X_test, y_test
        )
        print("Résultats :", resultats)

        # 7. Sauvegarder le modèle
        print("Sauvegarde du modèle...")
        modele.sauvegarder(
            CHEMIN_MODELE,
            {
                "algorithme": "Régression linéaire",
                "cible": "SalePrice",
                "variables": metadata,
                "evaluation": resultats
            }
        )
        print("Modèle sauvegardé avec succès !")

        # 8. Lancer l'interface graphique
        print("Ouverture de l'interface...")
        lancer(modele, metadata)

    except DonneeInvalideError as erreur:
        print(f"Erreur dans les données ou le modèle : {erreur}")

    except Exception as erreur:
        print(f"Une erreur est survenue : {erreur}")

if __name__ == "__main__":
    main()
