"""Interface graphique moderne de prédiction du prix des maisons."""

import csv
import math
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

RACINE = Path(__file__).resolve().parent.parent
FICHIER_HISTORIQUE = RACINE / "historique_predictions.csv"

BLEU_FONCE = "#172D4F"
BLEU = "#2563EB"
BLEU_CLAIR = "#EFF6FF"
FOND = "#F1F5F9"
BLANC = "#FFFFFF"
TEXTE = "#334155"
GRIS = "#64748B"
VERT = "#16A36A"
BORDURE = "#E2E8F0"


def lancer(modele, metadata):
    """Crée et lance l'application Tkinter."""

    numeriques = metadata["numeriques"]
    categorielles = metadata["categorielles"]

    fenetre = tk.Tk()
    fenetre.title("HomeValue - Estimation immobilière")
    fenetre.geometry("1150x950")
    fenetre.minsize(950, 750)
    fenetre.configure(bg=FOND)

    style = ttk.Style()
    style.theme_use("clam")

    # Style général
    style.configure(
        "TEntry",
        padding=9,
        font=("Segoe UI", 10),
        fieldbackground=BLANC,
        foreground=TEXTE
    )

    style.configure(
        "TCombobox",
        padding=9,
        font=("Segoe UI", 10),
        fieldbackground=BLANC
    )

    style.configure(
        "Treeview",
        font=("Segoe UI", 9),
        rowheight=30,
        background=BLANC,
        fieldbackground=BLANC
    )

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 9, "bold"),
        background=BLEU_CLAIR,
        foreground=BLEU_FONCE
    )

    # --------------------------------------------------
    # EN-TÊTE
    # --------------------------------------------------

    entete = tk.Frame(fenetre, bg=BLEU_FONCE, height=145)
    entete.pack(fill="x")
    entete.pack_propagate(False)

    tk.Label(
        entete,
        text="⌂  HOMEVALUE",
        bg=BLEU_FONCE,
        fg=BLANC,
        font=("Segoe UI", 13, "bold")
    ).pack(anchor="w", padx=35, pady=(15, 5))

    tk.Label(
        entete,
        text="Estimez le prix de votre maison",
        bg=BLEU_FONCE,
        fg=BLANC,
        font=("Segoe UI", 23, "bold")
    ).pack(anchor="w", padx=35)

    tk.Label(
        entete,
        text="Une estimation immobilière basée sur la régression linéaire.",
        bg=BLEU_FONCE,
        fg="#D5E1F0",
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=35, pady=5)

    # --------------------------------------------------
    # CONTENU AVEC DÉFILEMENT
    # --------------------------------------------------

    zone = tk.Frame(fenetre, bg=FOND)
    zone.pack(fill="both", expand=True)

    canvas = tk.Canvas(
        zone,
        bg=FOND,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        zone,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    contenu = tk.Frame(canvas, bg=FOND, padx=30, pady=20)

    fenetre_canvas = canvas.create_window(
        (0, 0),
        window=contenu,
        anchor="nw"
    )

    def ajuster_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def ajuster_largeur(event):
        canvas.itemconfigure(
            fenetre_canvas,
            width=event.width
        )

    contenu.bind("<Configure>", ajuster_scroll)
    canvas.bind("<Configure>", ajuster_largeur)

    # Défilement avec la molette
    def defiler(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all("<MouseWheel>", defiler)

    # --------------------------------------------------
    # TITRE DE SECTION
    # --------------------------------------------------

    tk.Label(
        contenu,
        text="Caractéristiques du bien",
        bg=FOND,
        fg=BLEU_FONCE,
        font=("Segoe UI", 16, "bold")
    ).pack(anchor="w", pady=(0, 5))

    tk.Label(
        contenu,
        text="Renseignez les informations pour obtenir une estimation.",
        bg=FOND,
        fg=GRIS,
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 15))

    # --------------------------------------------------
    # CARTE DES CHAMPS
    # --------------------------------------------------

    carte = tk.Frame(
        contenu,
        bg=BLANC,
        padx=22,
        pady=20,
        highlightbackground=BORDURE,
        highlightthickness=1
    )
    carte.pack(fill="x", pady=(0, 18))

    champs = {}

    def creer_champ(parent, nom, ligne, colonne, type_champ):
        """Crée un champ de saisie avec son titre."""

        bloc = tk.Frame(parent, bg=BLANC)
        bloc.grid(
            row=ligne,
            column=colonne,
            padx=12,
            pady=10,
            sticky="ew"
        )

        tk.Label(
            bloc,
            text=nom,
            bg=BLANC,
            fg=TEXTE,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(0, 7))

        if type_champ == "numerique":
            champ = ttk.Entry(bloc, font=("Segoe UI", 10))

            infos = numeriques[nom]

            indication = (
                f"Valeur entre {infos['min']:.0f} "
                f"et {infos['max']:.0f}"
            )

        else:
            champ = ttk.Combobox(
                bloc,
                values=categorielles[nom],
                state="readonly",
                font=("Segoe UI", 10)
            )

            indication = "Sélectionnez une option"

        champ.pack(fill="x", ipady=3)

        tk.Label(
            bloc,
            text=indication,
            bg=BLANC,
            fg=GRIS,
            font=("Segoe UI", 8)
        ).pack(anchor="w", pady=(4, 0))

        champs[nom] = champ

    carte.columnconfigure(0, weight=1)
    carte.columnconfigure(1, weight=1)

    # Sept variables numériques
    for i, nom in enumerate(numeriques):
        creer_champ(
            carte,
            nom,
            i // 2,
            i % 2,
            "numerique"
        )

    # Trois variables catégorielles
    for i, nom in enumerate(categorielles):
        creer_champ(
            carte,
            nom,
            4 + i // 2,
            i % 2,
            "categoriel"
        )

    # --------------------------------------------------
    # CARTE DU RÉSULTAT
    # --------------------------------------------------

    carte_resultat = tk.Frame(
        contenu,
        bg=BLEU_CLAIR,
        padx=20,
        pady=18,
        highlightbackground="#BFDBFE",
        highlightthickness=1
    )
    carte_resultat.pack(fill="x", pady=(0, 15))

    tk.Label(
        carte_resultat,
        text="PRIX ESTIMÉ DE LA MAISON",
        bg=BLEU_CLAIR,
        fg=BLEU_FONCE,
        font=("Segoe UI", 10, "bold")
    ).pack()

    resultat = tk.Label(
        carte_resultat,
        text="— $",
        bg=BLEU_CLAIR,
        fg=BLEU,
        font=("Segoe UI", 30, "bold")
    )
    resultat.pack(pady=5)

    texte_resultat = tk.Label(
        carte_resultat,
        text="Remplissez les champs pour commencer.",
        bg=BLEU_CLAIR,
        fg=GRIS,
        font=("Segoe UI", 9)
    )
    texte_resultat.pack()

    # --------------------------------------------------
    # ENREGISTREMENT DE L'HISTORIQUE
    # --------------------------------------------------

    def enregistrer_historique(donnees, prix):

        colonnes = [
            "date",
            *numeriques.keys(),
            *categorielles.keys(),
            "prix_predit"
        ]

        fichier_existe = FICHIER_HISTORIQUE.exists()

        with open(
            FICHIER_HISTORIQUE,
            "a",
            newline="",
            encoding="utf-8"
        ) as fichier:

            writer = csv.DictWriter(
                fichier,
                fieldnames=colonnes
            )

            if not fichier_existe:
                writer.writeheader()

            ligne = {
                "date": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                **donnees,
                "prix_predit": round(prix, 2)
            }

            writer.writerow(ligne)

    # --------------------------------------------------
    # FONCTION DE PRÉDICTION
    # --------------------------------------------------

    def predire():

        donnees = {}

        try:
            # Vérifier les variables numériques
            for nom, infos in numeriques.items():

                valeur = champs[nom].get().strip()

                if not valeur:
                    raise ValueError(
                        f"Veuillez remplir le champ {nom}."
                    )

                nombre = float(valeur.replace(",", "."))

                if not math.isfinite(nombre):
                    raise ValueError(
                        f"Valeur invalide pour {nom}."
                    )

                if infos["type"] == "int" and not nombre.is_integer():
                    raise ValueError(
                        f"{nom} doit être un nombre entier."
                    )

                if not infos["min"] <= nombre <= infos["max"]:
                    raise ValueError(
                        f"{nom} doit être compris entre "
                        f"{infos['min']:.0f} et {infos['max']:.0f}."
                    )

                donnees[nom] = (
                    int(nombre)
                    if infos["type"] == "int"
                    else nombre
                )

            # Vérifier les variables catégorielles
            for nom, options in categorielles.items():

                valeur = champs[nom].get()

                if not valeur:
                    raise ValueError(
                        f"Veuillez sélectionner {nom}."
                    )

                if valeur not in options:
                    raise ValueError(
                        f"Valeur invalide pour {nom}."
                    )

                donnees[nom] = valeur

            # Créer le DataFrame
            entree = pd.DataFrame([donnees])

            # Effectuer la prédiction
            prix = modele.predire(entree)

            if not math.isfinite(prix):
                raise ValueError(
                    "Le modèle a produit un résultat invalide."
                )

            # Afficher le résultat
            resultat.config(
                text=f"{prix:,.0f} $".replace(",", " ")
            )

            texte_resultat.config(
                text="Estimation calculée avec succès.",
                fg=VERT
            )

            # Enregistrer
            enregistrer_historique(donnees, prix)

        except ValueError as erreur:
            messagebox.showwarning(
                "Vérification des données",
                str(erreur)
            )

        except Exception as erreur:
            messagebox.showerror(
                "Erreur",
                f"Une erreur est survenue : {erreur}"
            )

    # --------------------------------------------------
    # BOUTONS
    # --------------------------------------------------

    boutons = tk.Frame(contenu, bg=FOND)
    boutons.pack(fill="x", pady=(0, 20))

    bouton_predire = tk.Button(
        boutons,
        text="✦  ESTIMER LE PRIX",
        command=predire,
        bg=BLEU,
        fg=BLANC,
        activebackground="#1D4ED8",
        activeforeground=BLANC,
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        cursor="hand2",
        padx=25,
        pady=12,
        bd=0
    )
    bouton_predire.pack(side="left", expand=True, fill="x", padx=5)

    def reinitialiser():

        for champ in champs.values():
            champ.delete(0, tk.END)

        resultat.config(text="— $")

        texte_resultat.config(
            text="Remplissez les champs pour commencer.",
            fg=GRIS
        )

    bouton_reset = tk.Button(
        boutons,
        text="Réinitialiser",
        command=reinitialiser,
        bg=BLANC,
        fg=BLEU_FONCE,
        activebackground=BLEU_CLAIR,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=12,
        bd=0,
        highlightbackground=BORDURE,
        highlightthickness=1
    )
    bouton_reset.pack(side="right", padx=5)

    # --------------------------------------------------
    # GRAPHIQUE MATPLOTLIB
    # --------------------------------------------------

    carte_graphique = tk.Frame(
        contenu,
        bg=BLANC,
        padx=18,
        pady=15,
        highlightbackground=BORDURE,
        highlightthickness=1
    )
    carte_graphique.pack(fill="x", pady=(0, 18))

    tk.Label(
        carte_graphique,
        text="Analyse des variables du modèle",
        bg=BLANC,
        fg=BLEU_FONCE,
        font=("Segoe UI", 13, "bold")
    ).pack(anchor="w", pady=(0, 10))

    try:
        pipeline = modele._pipeline

        preparation = pipeline.named_steps["preparation"]
        regression = pipeline.named_steps["regression"]

        noms = preparation.get_feature_names_out()
        coefficients = regression.coef_

        import numpy as np

        indices = np.argsort(
            np.abs(coefficients)
        )[-10:]

        figure = Figure(
            figsize=(9, 4),
            dpi=100,
            facecolor=BLANC
        )

        graphique = figure.add_subplot(111)

        graphique.barh(
            [noms[i].replace("num__", "").replace("cat__", "") for i in indices],
            [coefficients[i] for i in indices],
            color=BLEU
        )

        graphique.set_title(
            "Les 10 coefficients les plus importants",
            fontsize=11
        )

        graphique.set_xlabel(
            "Valeur du coefficient",
            fontsize=9
        )

        graphique.axvline(
            x=0,
            linewidth=0.8,
            color=GRIS
        )

        graphique.tick_params(labelsize=8)
        graphique.grid(axis="x", alpha=0.2)
        graphique.set_axisbelow(True)

        figure.tight_layout()

        graphique_canvas = FigureCanvasTkAgg(
            figure,
            master=carte_graphique
        )

        graphique_canvas.draw()

        graphique_canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    except Exception as erreur:

        tk.Label(
            carte_graphique,
            text=f"Graphique indisponible : {erreur}",
            bg=BLANC,
            fg=GRIS
        ).pack()

    # --------------------------------------------------
    # HISTORIQUE
    # --------------------------------------------------

    def consulter_historique():

        if not FICHIER_HISTORIQUE.exists():
            messagebox.showinfo(
                "Historique",
                "Aucune prédiction enregistrée."
            )
            return

        fenetre_historique = tk.Toplevel(fenetre)
        fenetre_historique.title("Historique des prédictions")
        fenetre_historique.geometry("950x450")
        fenetre_historique.configure(bg=FOND)

        tk.Label(
            fenetre_historique,
            text="Historique des estimations",
            bg=FOND,
            fg=BLEU_FONCE,
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", padx=20, pady=15)

        cadre_tableau = tk.Frame(
            fenetre_historique,
            bg=BLANC,
            padx=10,
            pady=10
        )
        cadre_tableau.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        with open(
            FICHIER_HISTORIQUE,
            newline="",
            encoding="utf-8"
        ) as fichier:

            lecteur = csv.DictReader(fichier)
            colonnes = lecteur.fieldnames

            tableau = ttk.Treeview(
                cadre_tableau,
                columns=colonnes,
                show="headings"
            )

            for colonne in colonnes:
                tableau.heading(
                    colonne,
                    text=colonne
                )

                tableau.column(
                    colonne,
                    width=115,
                    anchor="center"
                )

            for ligne in lecteur:
                tableau.insert(
                    "",
                    "end",
                    values=[ligne[c] for c in colonnes]
                )

        scrollbar_y = ttk.Scrollbar(
            cadre_tableau,
            orient="vertical",
            command=tableau.yview
        )

        scrollbar_x = ttk.Scrollbar(
            cadre_tableau,
            orient="horizontal",
            command=tableau.xview
        )

        tableau.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        tableau.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        cadre_tableau.rowconfigure(0, weight=1)
        cadre_tableau.columnconfigure(0, weight=1)

    bouton_historique = tk.Button(
        contenu,
        text="◷  Consulter l'historique des prédictions",
        command=consulter_historique,
        bg=BLANC,
        fg=BLEU,
        activebackground=BLEU_CLAIR,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=12,
        bd=0,
        highlightbackground=BORDURE,
        highlightthickness=1
    )

    bouton_historique.pack(fill="x", pady=(0, 15))

    # --------------------------------------------------
    # AVERTISSEMENT
    # --------------------------------------------------

    tk.Label(
        contenu,
        text=(
            "AVERTISSEMENT : cette application est un outil pédagogique. "
            "Le prix affiché est une estimation et ne constitue pas "
            "une évaluation immobilière officielle."
        ),
        bg=FOND,
        fg=GRIS,
        font=("Segoe UI", 9),
        wraplength=950,
        justify="center"
    ).pack(pady=(5, 15))

    # Lancement
    fenetre.mainloop()

