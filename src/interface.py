"""Interface graphique (Tkinter) : estimation du prix d'une maison."""
import math
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, List, Optional
 
import pandas as pd
 
from donnees import COLONNES_CATEGORIELLES, COLONNES_NUMERIQUES
from exceptions import DonneeInvalideError, ModeleIndisponibleError
from modele import Modele
 
ETIQUETTES = {
    "OverallQual": "Qualité générale (1 à 10)",
    "GrLivArea": "Surface habitable (pi²)",
    "TotalBsmtSF": "Surface du sous-sol (pi²)",
    "GarageCars": "Places de garage",
    "YearBuilt": "Année de construction",
    "FullBath": "Salles de bain complètes",
    "LotArea": "Superficie du terrain (pi²)",
    "Neighborhood": "Quartier",
    "KitchenQual": "Qualité de la cuisine",
    "CentralAir": "Climatisation centrale",
}
 
# Texte affiché -> code du jeu de données (les autres valeurs restent telles quelles)
AFFICHAGE = {
    "KitchenQual": {"Ex": "Excellente", "Gd": "Bonne", "TA": "Moyenne",
                    "Fa": "Passable", "Po": "Mauvaise"},
    "CentralAir": {"Y": "Oui", "N": "Non"},
}
 
 
def convertir_numerique(nom: str, texte: str, infos: dict):
    """Convertit le texte saisi en nombre (int ou float) ou lève DonneeInvalideError."""
    etiquette = ETIQUETTES[nom]
    texte = texte.strip().replace(",", ".")
    if not texte:
        raise DonneeInvalideError(f"« {etiquette} » est vide.")
    try:
        valeur = float(texte)
    except ValueError:
        raise DonneeInvalideError(f"« {etiquette} » doit être un nombre.") from None
    if not math.isfinite(valeur):
        raise DonneeInvalideError(f"« {etiquette} » doit être un nombre fini.")
    if infos["type"] == "int":
        if valeur != int(valeur):
            raise DonneeInvalideError(f"« {etiquette} » doit être un nombre entier.")
        return int(valeur)
    return valeur
 
 
def hors_plage(valeur: float, infos: dict) -> bool:
    """Vrai si la valeur sort de l'intervalle observé à l'entraînement."""
    return not infos["min"] <= valeur <= infos["max"]
 
 
def construire_ligne(valeurs: Dict[str, object]) -> pd.DataFrame:
    """Met les valeurs saisies dans un DataFrame d'une ligne, colonnes dans le bon ordre."""
    return pd.DataFrame([valeurs], columns=COLONNES_NUMERIQUES + COLONNES_CATEGORIELLES)
 
 
def formater_prix(montant: float) -> str:
    """Ex. 182500.4 -> '182 500 $'."""
    return f"{montant:,.0f}".replace(",", " ") + " $"
 
 
class Application(tk.Tk):
    """Fenêtre principale : formulaire de caractéristiques + prédiction."""
 
    def __init__(self, modele: Modele, description: dict,
                 rmse: Optional[float] = None) -> None:
        super().__init__()
        self.title("Estimation du prix d'une maison")
        self.resizable(False, False)
        self._modele = modele
        self._description = description
        self._rmse = rmse
        self._champs: Dict[str, tk.StringVar] = {}
        self._var_resultat = tk.StringVar(
            value="Remplissez les champs puis cliquez sur « Prédire ».")
        self._var_avertissement = tk.StringVar()
        self._construire_widgets()
        self.bind("<Return>", lambda _evt: self._predire())
 
    # ---------- construction ----------
    def _construire_widgets(self) -> None:
        cadre = ttk.Frame(self, padding=15)
        cadre.grid(sticky="nsew")
        ttk.Label(cadre, text="Caractéristiques de la maison",
                  font=("TkDefaultFont", 13, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")
 
        ligne = 1
        for nom in COLONNES_NUMERIQUES:
            infos = self._description["numeriques"][nom]
            var = tk.StringVar()
            self._champs[nom] = var
            ttk.Label(cadre, text=ETIQUETTES[nom]).grid(row=ligne, column=0, sticky="w", pady=3)
            ttk.Entry(cadre, textvariable=var, width=14).grid(row=ligne, column=1, padx=8)
            ttk.Label(cadre, foreground="gray",
                      text=f"entre {infos['min']:g} et {infos['max']:g}").grid(
                row=ligne, column=2, sticky="w")
            ligne += 1
 
        for nom in COLONNES_CATEGORIELLES:
            codes: List[str] = self._description["categorielles"][nom]
            affichage = AFFICHAGE.get(nom, {})
            var = tk.StringVar()
            self._champs[nom] = var
            ttk.Label(cadre, text=ETIQUETTES[nom]).grid(row=ligne, column=0, sticky="w", pady=3)
            ttk.Combobox(cadre, textvariable=var, state="readonly", width=12,
                         values=[affichage.get(c, c) for c in codes]).grid(
                row=ligne, column=1, padx=8)
            ligne += 1
 
        boutons = ttk.Frame(cadre)
        boutons.grid(row=ligne, column=0, columnspan=3, pady=12)
        ttk.Button(boutons, text="Prédire", command=self._predire).pack(side="left", padx=5)
        ttk.Button(boutons, text="Effacer", command=self._effacer).pack(side="left", padx=5)
 
        ttk.Label(cadre, textvariable=self._var_resultat, wraplength=380,
                  font=("TkDefaultFont", 12, "bold")).grid(
            row=ligne + 1, column=0, columnspan=3, sticky="w")
        ttk.Label(cadre, textvariable=self._var_avertissement, wraplength=380,
                  foreground="#b35900").grid(
            row=ligne + 2, column=0, columnspan=3, sticky="w", pady=(4, 0))
 
    # ---------- actions ----------
    def _lire_champs(self) -> Dict[str, object]:
        """Lit et valide tous les champs. Lève DonneeInvalideError au premier problème."""
        valeurs: Dict[str, object] = {}
        for nom in COLONNES_NUMERIQUES:
            infos = self._description["numeriques"][nom]
            valeurs[nom] = convertir_numerique(nom, self._champs[nom].get(), infos)
        for nom in COLONNES_CATEGORIELLES:
            choix = self._champs[nom].get()
            if not choix:
                raise DonneeInvalideError(f"Choisissez une valeur pour « {ETIQUETTES[nom]} ».")
            inverse = {texte: code for code, texte in AFFICHAGE.get(nom, {}).items()}
            valeurs[nom] = inverse.get(choix, choix)
        return valeurs
 
    def _predire(self) -> None:
        self._var_avertissement.set("")
        try:
            valeurs = self._lire_champs()
            prix = self._modele.predire(construire_ligne(valeurs))
        except (DonneeInvalideError, ModeleIndisponibleError) as erreur:
            messagebox.showerror("Entrée invalide", str(erreur), parent=self)
            return
 
        if prix <= 0:
            self._var_resultat.set("Estimation impossible pour cette combinaison.")
            self._var_avertissement.set(
                "Le modèle donne un prix négatif : ces caractéristiques sont trop "
                "éloignées des maisons connues.")
            return
 
        texte = f"Prix estimé : {formater_prix(prix)}"
        if self._rmse is not None:
            texte += f"\nErreur typique du modèle (RMSE) : ± {formater_prix(self._rmse)}"
        self._var_resultat.set(texte)
 
        sorties = [ETIQUETTES[n] for n in COLONNES_NUMERIQUES
                   if hors_plage(valeurs[n], self._description["numeriques"][n])]
        if sorties:
            self._var_avertissement.set(
                "Attention : valeur hors de l'intervalle connu pour " + ", ".join(sorties)
                + ". L'estimation est moins fiable.")
 
    def _effacer(self) -> None:
        for var in self._champs.values():
            var.set("")
        self._var_avertissement.set("")
        self._var_resultat.set("Remplissez les champs puis cliquez sur « Prédire ».")
 
 
def lancer(modele: Modele, description: dict, rmse: Optional[float] = None) -> None:
    """Ouvre la fenêtre et attend que l'utilisateur la ferme."""
    Application(modele, description, rmse).mainloop()
