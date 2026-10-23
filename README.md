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
README.md : présentation du projet
DECISIONS.md : décisions techniques
JOURNAL_IA.md : utilisation de l'IA
requirements.txt : dépendances Python

## Référence
Notebook Kaggle sur la prédiction du prix des maisons (voir le lien ci-dessus).
