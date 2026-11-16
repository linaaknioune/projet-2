Projet 2 INF1007 — Prédiction du prix des maisons
Description
Ce projet développe une application Python qui estime le prix de vente d'une maison à partir de ses caractéristiques. Les données proviennent du jeu de données immobilier House Prices disponible sur Kaggle. Une régression linéaire est entraînée avec scikit-learn, puis utilisée dans une interface graphique locale réalisée avec Tkinter. L'application permet de saisir les caractéristiques d'une maison et d'obtenir une estimation de son prix.

Cette application est un exercice pédagogique : ses estimations ne remplacent pas une évaluation immobilière professionnelle.
Jeu de données et problème
- Domaine : immobilier.
- Fichier : donnees/train.csv (1 460 observations dans le fichier d'origine).
- Cible : SalePrice, prix de vente à estimer (régression).
- Entrées : dix variables, dont sept numériques et trois catégorielles.
Variables numériques	Variables catégorielles
OverallQual, GrLivArea, TotalBsmtSF, GarageCars, YearBuilt, FullBath, LotArea	Neighborhood, KitchenQual, CentralAir


Source : Kaggle — House Prices: Advanced Regression Techniques. Un notebook Kaggle de référence a également été consulté.

Licence et redistribution : vérifier les conditions exactes d'utilisation et de redistribution du jeu de données sur sa page source avant de publier train.csv dans un dépôt public. Ne pas considérer « Kaggle » comme le nom d'une licence.
Préparation et entraînement
1. Charger le CSV avec pandas et vérifier les colonnes requises.
2. Supprimer les doublons, les cibles manquantes ou non positives et les maisons dont GrLivArea dépasse 4 000 pi².
3. Répartir les données en 80 % d'entraînement et 20 % de test, avec une graine fixe (42).
4. Remplacer les valeurs numériques manquantes par la médiane et les catégories manquantes par la modalité la plus fréquente ; encoder les catégories avec OneHotEncoder.
5. Entraîner une régression linéaire, calculer sa RMSE sur les données de test et la comparer à une référence qui prédit le prix moyen d'entraînement.
6. Sauvegarder le modèle dans Modeles/modele.joblib et les métadonnées (variables, valeurs admissibles, résultats) dans Modeles/modele.json.
Résultats
Les valeurs suivantes sont celles enregistrées dans le fichier Modeles/modele.json fourni avec le projet :
Évaluation sur l'ensemble de test	RMSE
Régression linéaire	26 527,24 $
Référence (prix moyen)	72 686,75 $


La RMSE mesure l'ampleur des erreurs de prédiction en dollars, avec une pénalisation plus importante des grosses erreurs. Le modèle fait mieux que la référence sur cette séparation des données. Ses prédictions restent approximatives et dépendent des caractéristiques disponibles et de la représentativité du jeu de données.
Interface graphique
L'interface Tkinter permet de saisir les caractéristiques numériques et catégorielles, de valider les saisies et d'afficher le prix estimé. Elle utilise les métadonnées du modèle sauvegardé. Le projet comprend également un graphique Matplotlib et un historique des prédictions. Vérifier ces fonctionnalités lors de la démonstration finale.
Technologies
Python, pandas, NumPy, scikit-learn, Matplotlib, Tkinter, joblib, pytest et coverage.
Installation et lancement
Depuis la racine du projet, avec Python installé :
python -m venv .venv
Sous Windows (PowerShell) :
.venv\Scripts\Activate.ps1
Installer les dépendances et lancer l'application :
python -m pip install -r requirements.txt
python src/main.py
Le programme charge les fichiers sauvegardés s'ils existent ; sinon, il entraîne et sauvegarde le modèle à partir de donnees/train.csv.
Tests et couverture
Exécuter les tests de logique avec :
python -m pytest
Mesurer la couverture :
python -m coverage run --source=src -m pytest test
python -m coverage report -m
Résultats obtenus (16 novembre 2026) : 41 tests réussis ; couverture totale de 28 % (520 instructions, 377 non couvertes).
Module	Couverture
src/donnees.py	100 %
src/exceptions.py	100 %
src/modele.py	100 %
src/exploration.py	0 %
src/interface.py	0 %
src/main.py	0 %
TOTAL	28 %


Les modules de traitement des données et de prédiction sont entièrement couverts par les tests exécutés. Les modules d'interface, d'exploration et de lancement ne sont pas couverts par cette exécution. L'énoncé demande de mesurer et de rapporter la couverture, sans imposer de seuil minimal.

Le dépôt contient un workflow GitHub Actions (.github/workflows/tests.yml) destiné à lancer les tests à chaque push. Vérifier que la dernière exécution est verte avant la remise.
Organisation du projet
projet-2-main/
├── .github/workflows/tests.yml
├── README.md
├── DECISIONS.md
├── JOURNAL_IA.md
├── requirements.txt
├── donnees/
│   └── train.csv
├── Modeles/
│   ├── modele.joblib
│   └── modele.json
├── src/
│   ├── donnees.py
│   ├── modele.py
│   ├── exceptions.py
│   ├── interface.py
│   └── main.py
├── test/
│   ├── test_donnees.py
│   └── test_modele.py
└── conftest.py
Le projet contient également un fichier Modeles.py à la racine, distinct du dossier Modeles/ et du module principal src/modele.py.
Conception du programme
Le code sépare la gestion des données, le modèle de prédiction et l'interface utilisateur. La classe JeuDeDonnees gère les données, tandis que Modele encapsule l'entraînement, l'évaluation et la prédiction. Le projet utilise des exceptions personnalisées pour signaler les données invalides. La RMSE est calculée à l'aide de NumPy.

Outil du chapitre 7 : à compléter après vérification de l'outil effectivement utilisé dans le code final (décorateur, générateur ou lambda) et de son utilité. La seule présence d'un import ne suffit pas.

POO : préciser ici les classes parentes et enfants réellement utilisées pour démontrer l'héritage et le polymorphisme, après vérification de leur implémentation finale.
Documentation officielle consultée ou à vérifier
- pandas — Getting started : lecture et manipulation des données.
- scikit-learn — Getting started : entraînement et évaluation d'un modèle.
- Python — tkinter : création de l'interface graphique.
Ces liens constituent des références adaptées au projet ; confirmer les pages réellement consultées avant la remise.
Justification des choix et utilisation de l'IA
Les choix techniques et leurs validations figurent dans DECISIONS.md. L'utilisation d'outils d'intelligence artificielle et les vérifications effectuées sont documentées dans JOURNAL_IA.md.
