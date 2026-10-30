# Prédiction du prix des maisons - projet 2

## Description
Ce projet vise à construire un modèle de machine learning capable de prédire le prix d'une maison à partir de caractéristiques
immobilières.
Le projet s'inspire de l'exercice Kaggle :
https://www.kaggle.com/code/michaelfumery/exercice-pr-diction-de-prix-de-maison/notebook

## Objectifs
- Explorer et comprendre les données.
- Nettoyer et préparer les données.
- Identifier les caractéristiques utiles.
- Entraîner un modèle de régression.
- Évaluer la qualité des prédictions.
- Visualiser les résultats.

## Technologies utilisées
- Python
- pandas
- NumPy
- scikit-learn
- Matplotlib
- pytest
- coverage

## Installation
```bash
pip install -r requirements.txt
```
## Exécution des tests 
```bash
pytest
```

## Couverture des tests
```bash
coverage run -m pytest
coverage report -m
```

## Organisation du projet

| Nom du fichier | Description |
|---|---|
| `README.md` | Documentation du projet |
| `DECISIONS.md` | Documentation des décisions prises |
| `JOURNAL_IA.md` |Journal d'utilisation de l'intelligence artificielle |
| `requirements.txt` | Liste des dépendances Python |
| `.github/workflows/tests.yml` | Lance pytest à chaque push |
| `donnees/` | Jeu de données (CSV) |
| `modeles/` | Modèle sauvegardé et métadonnées JSON |
| `src/donnees.py` | Lecture, nettoyage, classes de variables |
| `src/modele.py` | Entraînement, évaluation, prédiction |
| `src/exceptions.py` | Exceptions personnalisées |
| `src/interface.py` | Interface graphique |
| `src/main.py` | Point d'entrée |
| `tests/test_donnees.py` | Tests des données |
| `tests/test_modele.py` | Tests du modèle |

## Référence
Notebook Kaggle sur la prédiction du prix des maisons (voir le lien ci-dessus).
