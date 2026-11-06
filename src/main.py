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
 
 
a cintinuer
