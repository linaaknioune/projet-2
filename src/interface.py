import csv
import math
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

RACINE = Path(__file__).resolve().parent.parent
FICHIER_HISTORIQUE = RACINE / "historique_predictions.csv"

MARINE = "#0F172A"
MARINE_CLAIR = "#1E293B"
BLEU = "#2563EB"
BLEU_SURVOL = "#1D4ED8"
BLEU_CLAIR = "#EFF6FF"
FOND = "#F8FAFC"
BLANC = "#FFFFFF"
TEXTE = "#1E293B"
GRIS = "#64748B"
GRIS_CLAIR = "#94A3B8"
BORDURE = "#E2E8F0"
VERT = "#16A34A"
ROUGE = "#EF4444"
POLICE = "Segoe UI"

# COMPOSANTS PERSONNALISÉS
class BoutonArrondi(tk.Canvas):
    """Bouton à coins arrondis avec effet de survol."""
    def __init__(self, parent, texte, commande, couleur=BLEU,
                 survol=BLEU_SURVOL, texte_couleur=BLANC,
                 bordure=None, hauteur=46, rayon=12,
                 police=(POLICE, 10, "bold"), fond_parent=BLANC):
        super().__init__(parent, height=hauteur, bg=fond_parent, highlightthickness=0, cursor="hand2")
        self.texte = texte
        self.commande = commande
        self.couleur = couleur
        self.survol = survol
        self.texte_couleur = texte_couleur
        self.bordure = bordure
        self.rayon = rayon
        self.police = police
        self.actuelle = couleur
        self.bind("<Configure>", lambda e: self._dessiner())
        self.bind("<Enter>", lambda e: self._changer(self.survol))
        self.bind("<Leave>", lambda e: self._changer(self.couleur))
        self.bind("<ButtonRelease-1>", lambda e: self.commande())
    def _changer(self, couleur):
        self.actuelle = couleur
        self._dessiner()
    def _dessiner(self):
        self.delete("all")
        w, h, r = self.winfo_width(), self.winfo_height(), self.rayon
        if w < 2:
            return
        x1, y1, x2, y2 = 1, 1, w - 1, h - 1
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1
        ]
        self.create_polygon(points, smooth=True, fill=self.actuelle, outline=self.bordure or self.actuelle)
        self.create_text(w / 2, h / 2, text=self.texte, fill=self.texte_couleur, font=self.police)
def creer_carte(parent, **options):
    """Crée une carte blanche avec fine bordure."""
    return tk.Frame(parent, bg=BLANC, highlightbackground=BORDURE, highlightthickness=1, **options)

# APPLICATION
def lancer(modele, metadata):
    """Crée et lance l'application Tkinter."""
    numeriques = metadata["numeriques"]
    categorielles = metadata["categorielles"]
    fenetre = tk.Tk()
    fenetre.title("HomeValue - Estimation immobilière")
    fenetre.geometry("1280x820")
    fenetre.minsize(1050, 700)
    fenetre.configure(bg=FOND)

    # ---------- Styles ttk ----------
    style = ttk.Style()
    style.theme_use("clam")
    fenetre.option_add("*TCombobox*Listbox.font", (POLICE, 10))
    fenetre.option_add("*TCombobox*Listbox.selectBackground", BLEU)
    style.configure("M.TCombobox",font=(POLICE, 10),padding=9,fieldbackground=BLANC,background=BLANC,foreground=TEXTE,bordercolor=BORDURE,lightcolor=BLANC,darkcolor=BLANC,arrowcolor=GRIS,arrowsize=16)
    style.map("M.TCombobox",bordercolor=[("focus", BLEU)],fieldbackground=[("readonly", BLANC)],selectbackground=[("readonly", BLANC)],selectforeground=[("readonly", TEXTE)])
    style.configure("Treeview",font=(POLICE, 9),rowheight=32,background=BLANC,fieldbackground=BLANC,foreground=TEXTE,borderwidth=0)
    style.configure("Treeview.Heading",font=(POLICE, 9, "bold"),background=BLEU_CLAIR,foreground=MARINE,relief="flat",padding=8)
    style.map("Treeview", background=[("selected", BLEU)])
    style.configure("Vertical.TScrollbar",background=BORDURE,troughcolor=FOND,bordercolor=FOND,arrowcolor=GRIS,relief="flat")

    # ZONE PRINCIPALE AVEC DÉFILEMENT
    zone = tk.Frame(fenetre, bg=FOND)
    zone.pack(side="left", fill="both", expand=True)
    canvas = tk.Canvas(zone, bg=FOND, highlightthickness=0)
    scrollbar = ttk.Scrollbar(zone, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    contenu = tk.Frame(canvas, bg=FOND, padx=40, pady=30)
    fenetre_canvas = canvas.create_window((0, 0), window=contenu, anchor="nw")
    contenu.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfigure(fenetre_canvas, width=e.width))

    def defiler(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")
        elif sys.platform == "darwin":
            canvas.yview_scroll(int(-event.delta), "units")
        else:
            canvas.yview_scroll(int(-event.delta / 120), "units")

    def activer_molette(_):
        canvas.bind_all("<MouseWheel>", defiler)
        canvas.bind_all("<Button-4>", defiler)
        canvas.bind_all("<Button-5>", defiler)
    def desactiver_molette(_):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    canvas.bind("<Enter>", activer_molette)
    canvas.bind("<Leave>", desactiver_molette)

    # ---------- Titre ----------
    tk.Label(contenu, text="Estimer le prix d'un bien",bg=FOND, fg=MARINE, font=(POLICE, 24, "bold")).pack(anchor="w")
    tk.Label(contenu,text="Renseignez les caractéristiques pour obtenir " "une estimation basée sur la régression linéaire.",bg=FOND, fg=GRIS, font=(POLICE, 10)).pack(anchor="w", pady=(4, 24))

    # ---------- Grille deux colonnes ----------
    grille = tk.Frame(contenu, bg=FOND)
    grille.pack(fill="x")
    grille.columnconfigure(0, weight=3, uniform="col")
    grille.columnconfigure(1, weight=2, uniform="col")

    # CARTE FORMULAIRE
    carte_form = creer_carte(grille, padx=24, pady=22)
    carte_form.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
    carte_form.columnconfigure(0, weight=1, uniform="champ")
    carte_form.columnconfigure(1, weight=1, uniform="champ")
    champs = {}

    def titre_section(texte, ligne):
        tk.Label(carte_form, text=texte.upper(), bg=BLANC, fg=BLEU,font=(POLICE, 9, "bold")).grid(row=ligne, column=0, columnspan=2,sticky="w", padx=8, pady=(10, 0))
    def creer_champ(nom, ligne, colonne, type_champ):
        bloc = tk.Frame(carte_form, bg=BLANC)
        bloc.grid(row=ligne, column=colonne, padx=8, pady=9, sticky="ew")
        tk.Label(bloc, text=nom, bg=BLANC, fg=TEXTE, font=(POLICE, 10, "bold")).pack(anchor="w", pady=(0, 6))
        if type_champ == "numerique":
            # Bordure qui devient bleue au focus
            cadre = tk.Frame(bloc, bg=BORDURE, padx=1, pady=1)
            cadre.pack(fill="x")
            champ = tk.Entry(cadre, font=(POLICE, 10), relief="flat",bg=BLANC, fg=TEXTE, insertbackground=TEXTE,bd=0, highlightthickness=0)
            champ.pack(fill="x", ipady=8, padx=2)
            champ.bind("<FocusIn>", lambda e, c=cadre: c.config(bg=BLEU))
            champ.bind("<FocusOut>", lambda e, c=cadre: c.config(bg=BORDURE))
            infos = numeriques[nom]
            indication = (f"Entre {infos['min']:.0f} et {infos['max']:.0f}")
        else:
            champ = ttk.Combobox(bloc, values=categorielles[nom], state="readonly",style="M.TCombobox", font=(POLICE, 10))
            champ.pack(fill="x")
            indication = "Sélectionnez une option"
        tk.Label(bloc, text=indication, bg=BLANC, fg=GRIS_CLAIR,font=(POLICE, 8)).pack(anchor="w", pady=(4, 0))
        champs[nom] = champ
    ligne_courante = 0
    titre_section("Caractéristiques numériques", ligne_courante)
    ligne_courante += 1
    for i, nom in enumerate(numeriques):
        creer_champ(nom, ligne_courante + i // 2, i % 2, "numerique")
    ligne_courante += math.ceil(len(numeriques) / 2)
    titre_section("Informations complémentaires", ligne_courante)
    ligne_courante += 1
    for i, nom in enumerate(categorielles):
        creer_champ(nom, ligne_courante + i // 2, i % 2, "categoriel")
    ligne_courante += math.ceil(len(categorielles) / 2)

    # ---------- Boutons ----------
    zone_boutons = tk.Frame(carte_form, bg=BLANC)
    zone_boutons.grid(row=ligne_courante, column=0, columnspan=2,sticky="ew", padx=8, pady=(18, 0))
    zone_boutons.columnconfigure(0, weight=3)
    zone_boutons.columnconfigure(1, weight=1)
    colonne_droite = tk.Frame(grille, bg=FOND)
    colonne_droite.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
    carte_resultat = tk.Frame(colonne_droite, bg=MARINE, padx=26, pady=28)
    carte_resultat.pack(fill="x")
    tk.Label(carte_resultat, text="PRIX ESTIMÉ", bg=MARINE, fg=GRIS_CLAIR,font=(POLICE, 9, "bold")).pack(anchor="w")
    resultat = tk.Label(carte_resultat, text="— $", bg=MARINE, fg=BLANC,font=(POLICE, 38, "bold"))
    resultat.pack(anchor="w", pady=(8, 4))
    texte_resultat = tk.Label(carte_resultat,text="Remplissez le formulaire pour commencer.",bg=MARINE, fg=GRIS_CLAIR, font=(POLICE, 9),wraplength=300, justify="left")
    texte_resultat.pack(anchor="w")

    # ---------- Historique  ----------
    carte_historique = creer_carte(colonne_droite, padx=22, pady=18)
    carte_historique.pack(fill="x", pady=(16, 0))
    tk.Label(carte_historique, text="Historique des estimations",bg=BLANC, fg=MARINE, font=(POLICE, 11, "bold")).pack(anchor="w")
    tk.Label(carte_historique,text="Les plus récentes en premier. Cliquez sur une ligne ""pour voir le détail.",bg=BLANC, fg=GRIS, font=(POLICE, 9),wraplength=320, justify="left").pack(anchor="w", pady=(4, 10))
    cadre_tableau = tk.Frame(carte_historique, bg=BLANC)
    cadre_tableau.pack(fill="x")
    tableau = ttk.Treeview(cadre_tableau, columns=("date", "prix"),show="headings", height=7, selectmode="browse")
    tableau.heading("date", text="Date")
    tableau.heading("prix", text="Prix estimé")
    tableau.column("date", width=150, anchor="w")
    tableau.column("prix", width=110, anchor="e")
    tableau.tag_configure("pair", background=FOND)
    scroll_historique = ttk.Scrollbar(cadre_tableau, orient="vertical", command=tableau.yview)
    tableau.configure(yscrollcommand=scroll_historique.set)
    tableau.pack(side="left", fill="x", expand=True)
    scroll_historique.pack(side="right", fill="y")
    detail_historique = tk.Label(carte_historique, text="Aucune estimation pour l'instant.",bg=BLANC, fg=GRIS, font=(POLICE, 9),wraplength=320, justify="left")
    detail_historique.pack(anchor="w", pady=(10, 0))
    lignes_historique = {}
    def rafraichir_historique():
        tableau.delete(*tableau.get_children())
        lignes_historique.clear()
        if not FICHIER_HISTORIQUE.exists():
            return
        try:
            with open(FICHIER_HISTORIQUE, newline="", encoding="utf-8") as fichier:
                lignes = list(csv.DictReader(fichier))
        except Exception as erreur:
            detail_historique.config(text=f"Historique illisible : {erreur}", fg=GRIS)
            return
        for i, ligne in enumerate(reversed(lignes)):
            try:
                prix = formater(float(ligne["prix_predit"]))
            except (KeyError, ValueError):
                prix = "—"
            iid = tableau.insert("", "end",values=(ligne.get("date", ""), prix),tags=("pair",) if i % 2 == 0 else ())
            lignes_historique[iid] = ligne
        if lignes:
            detail_historique.config(text="Cliquez sur une ligne pour voir le détail.",fg=GRIS)
    def afficher_detail(_):
        selection = tableau.selection()
        if not selection:
            return
        ligne = lignes_historique.get(selection[0], {})
        morceaux = [
            f"{cle} : {valeur}" for cle, valeur in ligne.items()
            if cle not in ("date", "prix_predit")
        ]
        detail_historique.config(text="  ·  ".join(morceaux), fg=TEXTE)
    tableau.bind("<<TreeviewSelect>>", afficher_detail)

    # ---------- Animation du prix ----------
    jeton_animation = {"id": 0}
    def formater(valeur):
        return f"{valeur:,.0f} $".replace(",", " ")
    def animer_prix(cible, etape=0, total=24, jeton=None):
        if jeton is None:
            jeton_animation["id"] += 1
            jeton = jeton_animation["id"]
        if jeton != jeton_animation["id"]:
            return
        progression = 1 - (1 - etape / total) ** 3
        resultat.config(text=formater(cible * progression))
        if etape < total:
            fenetre.after(16, lambda: animer_prix(cible, etape + 1, total, jeton))

    # HISTORIQUE (ENREGISTREMENT)
    def enregistrer_historique(donnees, prix):
        colonnes = [
            "date",
            *numeriques.keys(),
            *categorielles.keys(),
            "prix_predit"
        ]
        fichier_existe = FICHIER_HISTORIQUE.exists()

        with open(FICHIER_HISTORIQUE, "a", newline="", encoding="utf-8") as fichier:
            writer = csv.DictWriter(fichier, fieldnames=colonnes)
            if not fichier_existe:
                writer.writeheader()

            writer.writerow({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **donnees,
                "prix_predit": round(prix, 2)
            })

    # PRÉDICTION
    def predire():
        donnees = {}
        try:
            for nom, infos in numeriques.items():
                valeur = champs[nom].get().strip()
                if not valeur:
                    raise ValueError(f"Veuillez remplir le champ {nom}.")
                nombre = float(valeur.replace(",", "."))
                if not math.isfinite(nombre):
                    raise ValueError(f"Valeur invalide pour {nom}.")
                if infos["type"] == "int" and not nombre.is_integer():
                    raise ValueError(f"{nom} doit être un nombre entier.")
                if not infos["min"] <= nombre <= infos["max"]:
                    raise ValueError(
                        f"{nom} doit être compris entre "
                        f"{infos['min']:.0f} et {infos['max']:.0f}."
                    )
                donnees[nom] = (int(nombre) if infos["type"] == "int" else nombre)
            for nom, options in categorielles.items():
                valeur = champs[nom].get()
                if not valeur:
                    raise ValueError(f"Veuillez sélectionner {nom}.")
                if valeur not in options:
                    raise ValueError(f"Valeur invalide pour {nom}.")
                donnees[nom] = valeur
            prix = modele.predire(pd.DataFrame([donnees]))
            if not math.isfinite(prix):
                raise ValueError("Le modèle a produit un résultat invalide.")
            animer_prix(prix)
            texte_resultat.config(text="✓  Estimation calculée à "f"{datetime.now().strftime('%H:%M')}.",fg="#4ADE80")
            enregistrer_historique(donnees, prix)
            rafraichir_historique()
        except ValueError as erreur:
            messagebox.showwarning("Vérification des données", str(erreur))
        except Exception as erreur:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {erreur}")
    def reinitialiser():
        for nom, champ in champs.items():
            if isinstance(champ, ttk.Combobox):
                champ.set("")
            else:
                champ.delete(0, tk.END)
        jeton_animation["id"] += 1
        resultat.config(text="— $")
        texte_resultat.config(text="Remplissez le formulaire pour commencer.",fg=GRIS_CLAIR)
    BoutonArrondi(zone_boutons, "✦   Estimer le prix", predire).grid(row=0, column=0, sticky="ew", padx=(0, 8))
    BoutonArrondi(zone_boutons, "Réinitialiser", reinitialiser,couleur=BLANC, survol=BLEU_CLAIR, texte_couleur=MARINE,bordure=BORDURE).grid(row=0, column=1, sticky="ew")
    fenetre.bind("<Return>", lambda e: predire())

    # GRAPHIQUE
    carte_graphique = creer_carte(contenu, padx=24, pady=20)
    carte_graphique.pack(fill="x", pady=(24, 0))
    tk.Label(carte_graphique, text="Analyse des variables du modèle",bg=BLANC, fg=MARINE, font=(POLICE, 13, "bold")).pack(anchor="w")
    tk.Label(carte_graphique,text="Les 10 coefficients ayant le plus d'influence ""(bleu : hausse du prix, rouge : baisse).",bg=BLANC, fg=GRIS, font=(POLICE, 9)).pack(anchor="w", pady=(2, 10))

    try:
        pipeline = modele._pipeline
        preparation = pipeline.named_steps["preparation"]
        regression = pipeline.named_steps["regression"]
        noms = preparation.get_feature_names_out()
        coefficients = np.ravel(regression.coef_)
        indices = np.argsort(np.abs(coefficients))[-10:]
        etiquettes = [
            noms[i].replace("num__", "").replace("cat__", "")
            for i in indices
        ]
        valeurs = [coefficients[i] for i in indices]
        couleurs = [BLEU if v >= 0 else ROUGE for v in valeurs]

        figure = Figure(figsize=(9, 4), dpi=100, facecolor=BLANC)
        graphique = figure.add_subplot(111)
        graphique.barh(etiquettes, valeurs, color=couleurs, height=0.65)
        graphique.axvline(x=0, linewidth=0.8, color=GRIS)
        graphique.set_xlabel("Valeur du coefficient", fontsize=9,color=GRIS)
        graphique.tick_params(labelsize=8, colors=GRIS, length=0)
        graphique.grid(axis="x", alpha=0.2)
        graphique.set_axisbelow(True)

        for cote in ("top", "right", "left"):
            graphique.spines[cote].set_visible(False)
        graphique.spines["bottom"].set_color(BORDURE)
        figure.tight_layout()
        graphique_canvas = FigureCanvasTkAgg(figure, master=carte_graphique)
        graphique_canvas.draw()
        graphique_canvas.get_tk_widget().pack(fill="both", expand=True)

    except Exception as erreur:
        tk.Label(carte_graphique, text=f"Graphique indisponible : {erreur}",bg=BLANC, fg=GRIS).pack()
    rafraichir_historique()

    # Espace en bas de page
    tk.Frame(contenu, bg=FOND, height=20).pack()
    fenetre.mainloop()
