
# Projet 2 - INF1007 Automne 2026

## Prédiction du prix des maisons

---

## Description

Ce projet consiste à développer une application Python permettant d'estimer le prix de vente d'une maison à partir de ses caractéristiques.

Les données proviennent du jeu de données **House Prices** disponible sur Kaggle. Un modèle de régression linéaire est entraîné avec la bibliothèque `scikit-learn`, puis utilisé dans une interface graphique développée avec `Tkinter`.

L'utilisateur peut saisir les caractéristiques d'une maison et obtenir une estimation de son prix.

Cette application est réalisée dans un cadre pédagogique. Les prédictions ne remplacent pas une évaluation immobilière professionnelle.

---

## 1. Jeu de données

### Domaine

Le domaine choisi est **l'immobilier**.

### Source des données

Le jeu de données provient de Kaggle :

[House Prices - Advanced Regression Techniques](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data)

Un notebook Kaggle a également été consulté :

[Exercice de prédiction de prix de maison](https://www.kaggle.com/code/michaelfumery/exercice-pr-diction-de-prix-de-maison/notebook)

**Licence :** les conditions d'utilisation et de redistribution doivent être vérifiées sur la page source avant la publication des données dans un dépôt public.

### Caractéristiques du jeu de données

- **Fichier :** `donnees/train.csv`
- **Nombre d'observations :** 1 460 dans le fichier d'origine.
- **Variable cible :** `SalePrice`
- **Type de problème :** régression.
- **Nombre de variables d'entrée :** 10.

### Variables utilisées

| Variables numériques | Variables catégorielles |
|---|---|
| OverallQual | Neighborhood |
| GrLivArea | KitchenQual |
| TotalBsmtSF | CentralAir |
| GarageCars | |
| YearBuilt | |
| FullBath | |
| LotArea | |

Les variables numériques représentent des caractéristiques mesurables de la maison, tandis que les variables catégorielles décrivent notamment son quartier et certains équipements.

---

## 2. Préparation des données

Les données sont chargées et préparées avec `pandas`.

Les principales étapes sont :

1. Charger le fichier CSV.
2. Vérifier la présence des colonnes nécessaires.
3. Supprimer les doublons.
4. Supprimer les observations dont le prix est manquant ou invalide.
5. Retirer les maisons dont `GrLivArea` dépasse 4 000 pieds carrés.
6. Traiter les valeurs manquantes.
7. Séparer les données en ensembles d'entraînement et de test.

Les données sont réparties comme suit :

- **80 %** pour l'entraînement.
- **20 %** pour les tests.
- **Graine aléatoire :** `42`.

Les valeurs numériques manquantes sont remplacées par la médiane. Les valeurs catégorielles manquantes sont remplacées par la catégorie la plus fréquente.

Les catégories sont transformées avec `OneHotEncoder`.

---

## 3. Modèle de prédiction

### Modèle utilisé

Le modèle choisi est une **régression linéaire**, implémentée avec `scikit-learn`.

Il permet d'estimer le prix d'une maison en fonction des dix variables sélectionnées.

### Métrique d'évaluation

La métrique utilisée est la **RMSE** (*Root Mean Squared Error*).

Elle mesure l'erreur de prédiction du modèle en dollars.

Plus la RMSE est faible, plus les prédictions sont proches des valeurs réelles selon cette métrique.

### Résultats obtenus

| Modèle | RMSE |
|---|---:|
| Régression linéaire | 26 527,24 $ |
| Modèle de référence (prix moyen) | 72 686,75 $ |

Le modèle de régression linéaire obtient une erreur inférieure à celle du modèle de référence.

Ces résultats montrent que le modèle exploite les caractéristiques des maisons pour améliorer les estimations par rapport à une prédiction basée uniquement sur le prix moyen.

Cependant, les prédictions restent approximatives et dépendent des données utilisées pour l'entraînement.

### Sauvegarde du modèle

Après l'entraînement, deux fichiers sont générés :

- `Modeles/modele.joblib` : contient le modèle entraîné.
- `Modeles/modele.json` : contient les métadonnées du modèle.

Ces métadonnées comprennent les variables d'entrée, les catégories possibles, les intervalles numériques et les résultats de l'évaluation.

---

## 4. Interface graphique

L'interface graphique est développée avec `Tkinter`.

Elle permet à l'utilisateur de saisir les caractéristiques d'une maison et de demander une prédiction.

### Fonctionnalités

- Saisie des variables numériques.
- Sélection des variables catégorielles.
- Validation des saisies.
- Affichage du prix estimé.
- Affichage d'un graphique avec `Matplotlib`.
- Enregistrement des prédictions dans un historique.
- Consultation de l'historique des prédictions.

Les saisies invalides sont traitées afin d'éviter les erreurs lors de l'utilisation de l'application.

L'interface utilise les métadonnées enregistrées avec le modèle.

---

## 5. Organisation du projet

```text
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
```

### Description des principaux fichiers

- **donnees.py :** chargement, nettoyage et séparation des données.
- **modele.py :** entraînement, évaluation et prédiction.
- **exceptions.py :** gestion des exceptions personnalisées.
- **exploration.py :** exploration graphique des données.
- **interface.py :** interface graphique de l'application.
- **main.py :** point d'entrée du programme.
- **test/ :** tests automatisés avec pytest.
- **DECISIONS.md :** justification des choix du projet.
- **JOURNAL_IA.md :** documentation de l'utilisation de l'intelligence artificielle.

---

## 6. Programmation orientée objet

Le projet utilise plusieurs classes pour organiser le programme.

### Classes principales

- `JeuDeDonnees` : gère le chargement et le nettoyage des données.
- `Modele` : gère l'entraînement, l'évaluation et les prédictions.
- `BoutonArrondi` : représente un bouton personnalisé dans l'interface graphique.

### Héritage

La classe `BoutonArrondi` hérite de `tk.Canvas`.

Elle réutilise les fonctionnalités de la classe parente pour créer un bouton graphique personnalisé.

### Polymorphisme

L'exigence de polymorphisme doit encore être vérifiée dans le code final.

L'énoncé demande une classe parente et au moins deux classes enfants qui redéfinissent une même méthode.

### Encapsulation et composition

La classe `Modele` regroupe les opérations liées au modèle de prédiction.

L'application utilise les objets et les modules du projet pour relier les données, les prédictions et l'interface graphique.

---

## 7. Fonctions avancées - Chapitre 7

Le projet utilise des fonctions `lambda` dans `interface.py`.

Ces fonctions permettent notamment d'associer des actions aux événements des boutons de l'interface graphique.

La fonction `animer_prix()` utilise également des appels successifs programmés avec `fenetre.after()` pour animer l'affichage du prix.

Ces outils permettent de simplifier la gestion des événements et d'améliorer l'interactivité de l'application.

---

## 8. Tests automatisés

Les tests sont réalisés avec la bibliothèque `pytest`.

Ils permettent de vérifier le fonctionnement des fonctions principales du projet.

### Résultats des tests

**41 tests ont été exécutés avec succès.**

```text
41 passed in 5.81s
```

Les tests couvrent notamment :

- Le chargement des données.
- Le nettoyage des données.
- La séparation des données.
- Le fonctionnement du modèle.
- Les prédictions.
- La gestion des erreurs.

### Couverture du code

La couverture a été mesurée avec `coverage`.

| Fichier | Couverture |
|---|---:|
| donnees.py | 100 % |
| exceptions.py | 100 % |
| modele.py | 100 % |
| exploration.py | 0 % |
| interface.py | 0 % |
| main.py | 0 % |
| **TOTAL** | **28 %** |

Les modules principaux de traitement des données et de prédiction sont entièrement couverts par les tests.

La couverture totale est de **28 %**, principalement parce que les fichiers liés à l'interface graphique, à l'exploration et au lancement de l'application ne sont pas exécutés par ces tests.

L'énoncé ne fixe aucun pourcentage minimum de couverture.

### Commandes pour exécuter les tests

```bash
python -m pytest test
```

### Commandes pour mesurer la couverture

```bash
python -m coverage run --source=src -m pytest test
python -m coverage report -m
```

---

## 9. GitHub et intégration continue

Le projet utilise GitHub pour le suivi du développement.

Un workflow GitHub Actions est présent dans :

`.github/workflows/tests.yml`

Il permet de lancer automatiquement les tests lors des modifications envoyées sur le dépôt.

La dernière exécution doit être vérifiée dans l'onglet **Actions** avant la remise.

---

## 10. Installation et exécution

### Prérequis

- Python installé.
- VS Code ou un autre environnement Python.
- Les bibliothèques nécessaires au projet.

### Installation

**1. Créer un environnement virtuel :**

```bash
python -m venv .venv
```

**2. Activer l'environnement sous Windows :**

```powershell
.venv\Scripts\Activate.ps1
```

**3. Installer les bibliothèques :**

```bash
python -m pip install -r requirements.txt
```

**4. Lancer l'application :**

```bash
python src/main.py
```

Le programme charge le modèle sauvegardé lorsqu'il est disponible. Sinon, il peut entraîner un nouveau modèle à partir du fichier `train.csv`.

---

## 11. Bibliothèques utilisées

| Bibliothèque | Utilisation |
|---|---|
| pandas | Chargement et traitement des données |
| NumPy | Calculs numériques |
| scikit-learn | Entraînement et évaluation du modèle |
| Matplotlib | Création des graphiques |
| Tkinter | Interface graphique |
| joblib | Sauvegarde du modèle |
| pytest | Tests automatisés |
| coverage | Mesure de la couverture des tests |

---

## 12. Documentation officielle

Les documentations suivantes servent de références techniques au projet :

- [Documentation pandas](https://pandas.pydata.org/docs/getting_started/index.html)
- [Documentation scikit-learn](https://scikit-learn.org/stable/getting_started.html)
- [Documentation Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Documentation Matplotlib](https://matplotlib.org/stable/)
- [Documentation pytest](https://docs.pytest.org/)

Les références effectivement consultées doivent être confirmées avant la remise.

---

## 13. Décisions et utilisation de l'intelligence artificielle

Les choix techniques réalisés pendant le projet sont documentés dans le fichier :

`DECISIONS.md`

Ce document présente les différentes options envisagées, les choix retenus, leurs justifications et les validations obtenues auprès de l'auxiliaire.

L'utilisation de l'intelligence artificielle est documentée dans :

`JOURNAL_IA.md`

Ce journal présente les demandes effectuées, les réponses reçues, les vérifications réalisées et les décisions prises.

---

## Conclusion

Ce projet a permis de développer une application Python qui combine le traitement des données, l'apprentissage automatique et une interface graphique.

Le modèle de régression linéaire permet d'estimer le prix d'une maison à partir de plusieurs caractéristiques.

Les tests automatisés contribuent à vérifier le fonctionnement des principales fonctions du programme.

Le projet met également en pratique plusieurs notions du cours INF1007, notamment les fichiers, les fonctions, les modules, la programmation orientée objet, les exceptions, les tests et les bibliothèques Python.

