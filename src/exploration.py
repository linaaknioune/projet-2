
import os
import matplotlib.pyplot as plt

from donnees import JeuDeDonnees

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(RACINE, "donnees", "train.csv")
DOSSIER_GRAPHIQUES = os.path.join(RACINE, "Modeles")


def creer_graphique() -> None:
    """Crée et enregistre la distribution des prix des maisons."""
    jeu = JeuDeDonnees(CSV)
    jeu.charger()
    jeu.nettoyer()

    prix = jeu.df["SalePrice"]

    os.makedirs(DOSSIER_GRAPHIQUES, exist_ok=True)

    plt.figure(figsize=(9, 5))
    plt.hist(prix, bins=30, edgecolor="black")
    plt.title("Distribution des prix des maisons")
    plt.xlabel("Prix de vente")
    plt.ylabel("Nombre de maisons")
    plt.tight_layout()

    chemin = os.path.join(DOSSIER_GRAPHIQUES, "distribution_prix.png")
    plt.savefig(chemin)
    plt.close()

    print("Graphique enregistré :", chemin)


if __name__ == "__main__":
    print("Début de la création du graphique")
    creer_graphique()
