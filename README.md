
# Projet 2 – INF1007 Automne 2026

## Prédiction du prix des maisons

---

## 1. Description du projet

Ce projet consiste à développer une application Python permettant d'estimer le prix de vente d'une maison à partir de ses caractéristiques.

Le projet utilise un jeu de données immobilier provenant de Kaggle. Un modèle de régression linéaire est entraîné avec la bibliothèque `scikit-learn`, puis intégré à une interface graphique développée avec `Tkinter`.

L'application permet à l'utilisateur de saisir les caractéristiques d'une maison, d'obtenir une estimation de son prix et de consulter un graphique ainsi que l'historique des prédictions.

L'objectif est de mettre en pratique les notions de programmation Python, de traitement des données, d'apprentissage automatique et de développement d'interfaces graphiques.

---

## 2. Jeu de données

### Domaine choisi

Le domaine retenu est l'immobilier. L'application répond à la question suivante :

**Quel est le prix de vente estimé d'une maison selon ses caractéristiques ?**

### Source des données

Le jeu de données utilisé est **House Prices – Advanced Regression Techniques**, disponible sur Kaggle.

- [Jeu de données Kaggle](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data)
- [Notebook Kaggle de référence](https://www.kaggle.com/code/michaelfumery/exercice-pr-diction-de-prix-de-maison/notebook)

### Caractéristiques du jeu de données

- **Format :** CSV
- **Fichier :** `donnees/train.csv`
- **Nombre d'observations initiales :** 1 460
- **Variable cible :** `SalePrice`
- **Type de problème :** régression
- **Nombre de variables d'entrée :** 10

### Variables utilisées

| Variable | Type | Description |
|---|---|---|
| OverallQual | Numérique | Qualité générale de la maison |
| GrLivArea | Numérique | Surface habitable au-dessus du sol |
| TotalBsmtSF | Numérique | Surface totale du sous-sol |
| GarageCars | Numérique | Capacité du garage |
| YearBuilt | Numérique | Année de construction |
| FullBath | Numérique | Nombre de salles de bain complètes |
| LotArea | Numérique | Superficie du terrain |
| Neighborhood | Catégorielle | Quartier de la maison |
| KitchenQual | Catégorielle | Qualité de la cuisine |
| CentralAir | Catégorielle | Présence de climatisation centrale |

Le jeu de données contient des variables numériques et catégorielles permettant d'estimer le prix de vente des maisons.

---

## 3. Préparation et nettoyage des données

Les données sont chargées et traitées à l'aide de la bibliothèque `pandas`.

La classe `JeuDeDonnees`, définie dans `donnees.py`, assure le chargement, la vérification et le nettoyage des données.

### Nettoyage effectué

Les opérations suivantes sont réalisées :

1. Vérification de l'existence du fichier CSV.
2. Vérification des colonnes nécessaires.
3. Suppression des doublons.
4. Suppression des observations dont le prix de vente est manquant ou inférieur ou égal à zéro.
5. Suppression des observations dont `GrLivArea` dépasse 4 000 pieds carrés.
6. Traitement des valeurs manquantes.
7. Préparation des variables pour l'entraînement.

Les valeurs numériques manquantes sont remplacées par la médiane, tandis que les valeurs catégorielles manquantes sont remplacées par la catégorie la plus fréquente.

Les variables catégorielles sont transformées à l'aide de `OneHotEncoder`.

### Séparation des données

Les données sont séparées avec `train_test_split` :

- **80 % :** ensemble d'entraînement.
- **20 % :** ensemble de test.
- **Graine aléatoire :** `42`.

Cette séparation permet d'évaluer le modèle sur des données différentes de celles utilisées pour son entraînement.

---

## 4. Modèle de prédiction

### Modèle retenu

Le modèle utilisé est une **régression linéaire** implémentée avec `scikit-learn`.

Ce modèle estime le prix d'une maison à partir des dix variables sélectionnées.

La classe `Modele`, définie dans `modele.py`, regroupe les principales opérations :

- Création du pipeline de traitement.
- Entraînement du modèle.
- Évaluation des prédictions.
- Calcul de la métrique.
- Sauvegarde et chargement du modèle.

### Métrique d'évaluation

La métrique choisie est la **RMSE (Root Mean Squared Error)**.

Elle mesure l'écart entre les prix prédits et les prix réels en accordant davantage de poids aux erreurs importantes.

Une RMSE plus faible indique une meilleure précision selon cette métrique.

### Modèle de référence

Un modèle de référence prédit systématiquement le prix moyen des maisons de l'ensemble d'entraînement.

Il permet de comparer les performances de la régression linéaire à une méthode simple.

### Résultats obtenus

| Modèle | RMSE |
|---|---:|
| Régression linéaire | 26 527,24 $ |
| Modèle de référence | 72 686,75 $ |

Le modèle de régression linéaire obtient une RMSE inférieure à celle du modèle de référence.

Cette comparaison montre que les caractéristiques des maisons permettent d'améliorer les estimations par rapport à une prédiction basée uniquement sur le prix moyen.

### Limites du modèle

Les prédictions dépendent des caractéristiques disponibles et de la représentativité des données d'entraînement.

Certaines caractéristiques susceptibles d'influencer le prix d'une maison ne sont pas utilisées dans le modèle.

Les estimations restent donc approximatives et ne remplacent pas une évaluation immobilière professionnelle.

### Sauvegarde du modèle

Le modèle entraîné est sauvegardé dans le dossier `Modeles/`.

Deux fichiers sont utilisés :

- `modele.joblib` : modèle entraîné.
- `modele.json` : métadonnées du modèle.

Les métadonnées contiennent les noms des variables, les catégories possibles, les intervalles numériques et les résultats d'évaluation.

---

## 5. Interface graphique

L'interface graphique est développée avec la bibliothèque `Tkinter`.

Elle permet à l'utilisateur d'interagir avec le modèle sans utiliser directement le code Python.

### Fonctionnalités principales

- Saisie des caractéristiques numériques.
- Sélection des caractéristiques catégorielles.
- Validation des données saisies.
- Affichage du prix estimé.
- Affichage d'un graphique avec `Matplotlib`.
- Enregistrement des prédictions.
- Consultation de l'historique des prédictions.

### Validation des saisies

Les valeurs saisies sont vérifiées avant d'effectuer une prédiction.

La validation permet de détecter notamment :

- Les champs vides.
- Les valeurs non numériques.
- Les valeurs situées hors des intervalles autorisés.
- Les catégories invalides.

Les erreurs sont signalées à l'utilisateur par des messages adaptés.

### Historique des prédictions

Les prédictions sont enregistrées dans le fichier :

`historique_predictions.csv`

Cet historique permet de conserver les résultats des estimations précédentes et de les consulter depuis l'interface.

### Graphiques

Le projet utilise `Matplotlib` pour représenter graphiquement les données et les résultats.

Le module `exploration.py` permet de produire un graphique d'exploration de la distribution des prix.

L'interface graphique intègre également une représentation visuelle liée aux prédictions.

---

## 6. Organisation du projet

    projet-2-main/
    |
    |-- .github/
    |   |-- workflows/
    |       |-- tests.yml
    |
    |-- donnees/
    |   |-- train.csv
    |
    |-- Modeles/
    |   |-- modele.joblib
    |   |-- modele.json
    |
    |-- src/
    |   |-- donnees.py
    |   |-- modele.py
    |   |-- exceptions.py
    |   |-- exploration.py
    |   |-- interface.py
    |   |-- main.py
    |
    |-- test/
    |   |-- test_donnees.py
    |   |-- test_modele.py
    |
    |-- conftest.py
    |-- DECISIONS.md
    |-- JOURNAL_IA.md
    |-- README.md
    |-- requirements.txt
    |-- historique_predictions.csv

### Description des fichiers

| Fichier | Rôle |
|---|---|
| donnees.py | Chargement, nettoyage et séparation des données |
| modele.py | Entraînement, évaluation et prédiction |
| exceptions.py | Gestion des exceptions personnalisées |
| exploration.py | Exploration et visualisation des données |
| interface.py | Interface graphique |
| main.py | Point d'entrée de l'application |
| test_donnees.py | Tests des fonctions liées aux données |
| test_modele.py | Tests du modèle de prédiction |
| DECISIONS.md | Justification des choix techniques |
| JOURNAL_IA.md | Documentation de l'utilisation de l'IA |
| requirements.txt | Dépendances Python |

---

## 7. Conception et programmation orientée objet

Le projet utilise la programmation orientée objet pour organiser les différentes responsabilités du programme.

### Classes principales

**JeuDeDonnees**

Cette classe gère le chargement, la vérification, le nettoyage et l'accès aux données.

**Modele**

Cette classe regroupe les opérations liées à la création, à l'entraînement, à l'évaluation et à l'utilisation du modèle de prédiction.

**BoutonArrondi**

Cette classe permet de créer un bouton personnalisé dans l'interface graphique.

### Héritage

La classe `BoutonArrondi`, définie dans `interface.py`, hérite de la classe `tk.Canvas`.

Elle réutilise les fonctionnalités graphiques de sa classe parente pour construire un bouton personnalisé.

### Encapsulation

Les classes regroupent les données et les méthodes associées à leurs responsabilités.

La gestion des données, l'entraînement du modèle et l'affichage sont répartis dans des modules distincts.

### Composition

L'application associe les différentes composantes du projet afin de permettre à l'utilisateur d'interroger le modèle depuis l'interface graphique.

### Exceptions personnalisées

Le projet utilise l'exception `DonneeInvalideError` pour signaler les problèmes liés au chargement et à la validation des données.

La gestion des exceptions permet de traiter les erreurs de manière contrôlée.

---

## 8. Fonctions avancées – Chapitre 7

Le projet utilise des fonctions `lambda` dans le module `interface.py`.

Ces fonctions anonymes sont notamment utilisées pour associer des actions aux événements de l'interface graphique.

Elles permettent de transmettre des commandes aux boutons et de gérer les interactions avec l'utilisateur.

Le module utilise également la fonction `animer_prix()`, qui programme des appels successifs avec `fenetre.after()` pour produire une animation de l'affichage du prix.

---

## 9. Calculs numériques – NumPy

Le projet utilise `NumPy` pour effectuer des calculs numériques.

La bibliothèque intervient notamment dans le calcul de la RMSE.

Les opérations vectorisées permettent d'effectuer des calculs sur plusieurs valeurs sans utiliser une boucle Python explicite.

Ces calculs servent à évaluer les performances du modèle de prédiction.

---

## 10. Tests automatisés et couverture

Les tests automatisés sont réalisés avec `pytest`.

Ils permettent de vérifier le fonctionnement des principales fonctions de traitement des données et de prédiction.

### Résultats des tests

**44 tests ont été exécutés avec succès.**

    44 passed in 5.81s

Les tests portent notamment sur :

- Le chargement des données.
- La validation des colonnes.
- Le nettoyage des données.
- La séparation des ensembles d'entraînement et de test.
- L'entraînement du modèle.
- Le calcul des métriques.
- Les prédictions.
- La gestion des erreurs.

### Couverture du code

La couverture des tests a été mesurée avec `coverage`.

| Fichier | Couverture |
|---|---:|
| donnees.py | 100 % |
| exceptions.py | 100 % |
| modele.py | 100 % |
| exploration.py | 0 % |
| interface.py | 0 % |
| main.py | 0 % |
| **TOTAL** | **28 %** |

Les modules de traitement des données et de prédiction sont entièrement couverts par les tests automatisés.

La couverture totale est de **28 %**, car les modules liés à l'interface graphique, à l'exploration et au lancement de l'application ne sont pas exécutés par ces tests.

### Exécution des tests

Depuis la racine du projet :

    python -m pytest test

### Mesure de la couverture

    python -m coverage run --source=src -m pytest test
    python -m coverage report -m

---

## 11. GitHub et intégration continue

Le projet utilise GitHub pour la gestion du code source et le suivi des modifications.

Le dépôt comprend un workflow GitHub Actions :

`.github/workflows/tests.yml`

Ce workflow permet d'exécuter automatiquement les tests avec `pytest` lors des modifications envoyées sur GitHub.

Le fichier `requirements.txt` contient les dépendances nécessaires à l'installation du projet.

---

## 12. Installation et exécution

### Prérequis

- Python
- pip
- Les bibliothèques indiquées dans `requirements.txt`

### Installation

**1. Créer un environnement virtuel :**

    python -m venv .venv

**2. Activer l'environnement virtuel sous Windows :**

    .venv\Scripts\Activate.ps1

**3. Installer les dépendances :**

    python -m pip install -r requirements.txt

**4. Lancer l'application :**

    python src/main.py

Au lancement, le programme utilise le modèle sauvegardé lorsqu'il est disponible.

Si les fichiers du modèle sont absents, le programme entraîne un modèle à partir du jeu de données, puis sauvegarde les résultats.

---

## 13. Bibliothèques utilisées

| Bibliothèque | Utilisation |
|---|---|
| pandas | Chargement et nettoyage des données |
| NumPy | Calculs numériques |
| scikit-learn | Entraînement et évaluation du modèle |
| Matplotlib | Création des graphiques |
| Tkinter | Développement de l'interface graphique |
| joblib | Sauvegarde et chargement du modèle |
| pytest | Tests automatisés |
| coverage | Mesure de la couverture des tests |

---

## 14. Documentation et références

### Jeu de données

Kaggle, *House Prices – Advanced Regression Techniques*.

https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data

### Notebook de référence

Kaggle, *Exercice de prédiction de prix de maison*.

https://www.kaggle.com/code/michaelfumery/exercice-pr-diction-de-prix-de-maison/notebook

### Documentation pandas

https://pandas.pydata.org/docs/getting_started/index.html

### Documentation scikit-learn

https://scikit-learn.org/stable/getting_started.html

### Documentation Tkinter

https://docs.python.org/3/library/tkinter.html

### Documentation Matplotlib

https://matplotlib.org/stable/

### Documentation pytest

https://docs.pytest.org/

---

## 15. Décisions et utilisation de l'intelligence artificielle

### Fiche de décisions

Le fichier `DECISIONS.md` présente les principaux choix effectués durant le projet.

Il regroupe les options envisagées, les choix retenus, leurs justifications et les validations obtenues auprès de l'auxiliaire d'enseignement.

### Journal d'utilisation de l'IA

Le fichier `JOURNAL_IA.md` documente l'utilisation de l'intelligence artificielle durant le développement.

Il présente les demandes effectuées, les réponses reçues, les vérifications réalisées et les décisions prises après ces vérifications.

---

## Conclusion

Ce projet a permis de développer une application Python capable d'estimer le prix de vente d'une maison à partir de plusieurs caractéristiques.

Le traitement des données est réalisé avec `pandas`, tandis que la régression linéaire est entraînée et évaluée avec `scikit-learn`.

L'interface graphique développée avec `Tkinter` permet à l'utilisateur d'effectuer des prédictions et de consulter les résultats.

Les tests automatisés permettent de vérifier le fonctionnement des principales composantes du programme.

Le projet met en pratique plusieurs notions du cours INF1007, notamment la manipulation de fichiers, les fonctions, les modules, les exceptions, la programmation orientée objet, les calculs numériques et les tests automatisés.

