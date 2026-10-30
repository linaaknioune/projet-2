# Journal des décisions techniques

| Choix | Options envisagées | Choix retenu et justification | Validé par l'auxiliaire (date) |
|---|---|---|---|
| Domaine | Immobilier ; Transport ; Environnement et énergie | **Immobilier** : prédire le prix probable d'une maison. Domaine compréhensible par tous, pas de donnée sensible, un utilisateur peut tester des caractéristiques concrètes (qualité, surface, quartier, commerce à proximiter). | à remplir |
| Jeu de données | Kaggle : Prédiction de prix des maisons ; Kaggle : Données sur le transport de marchandises ; Kaggle : Données sur la fraude de carte de crédit | **Prédiction de prix des maisions, `train.csv`** 1 460 lignes (500 à 50 000 ✔), 79 colonnes d'entrée (≥ 5 ✔), cible `SalePrice` ✔, variables numériques et catégorielles ✔, aucune donnée personnelle ✔. Licence : **à confirmer sur la page Kaggle avant la validation**. | _à remplir_ |
| Choix des variables d'entrée | Les 79 colonnes ; sélection par corrélation ; sélection manuelle | **10 variables choisies à la main** (7 numériques : OverallQual, GrLivArea, TotalBsmtSF, GarageCars, YearBuilt, FullBath, LotArea ; 3 catégorielles : Neighborhood, KitchenQual, CentralAir). Une interface à 79 champs est inutilisable ; choisir selon des critères de domaine (variables qu'un acheteur connaît) évite de sélectionner d'après les données de test. | _à remplir_ |
| Nettoyage | Tout garder ; retirer les valeurs aberrantes | Retirer les maisons de plus de 4 000 pi² (recommandation de l'auteur du jeu, à vérifier dans son article), les doublons et les cibles invalides. Les valeurs manquantes sont imputées dans le pipeline (médiane / valeur la plus fréquente), apprises sur l'entraînement seulement, pour éviter toute fuite d'information. | _à remplir_ |
| Cible et métrique | RMSE ; MAE ; R² | **Cible `SalePrice`, régression. Métrique principale : RMSE en dollars** (même unité que le prix, pénalise les grosses erreurs). MAE et R² rapportés en complément. | _à remplir_ |
| Modèle | Régression linéaire ; forêt aléatoire ; k plus proches voisins | **Régression linéaire et forêt aléatoire comparées par validation croisée (5 blocs) sur l'entraînement seulement ; le meilleur est retenu.** Référence : prédire la moyenne. Le test n'est utilisé qu'une fois, à la fin. | _à remplir_ |
| Séparation | 80/20 ; 70/30 | 80/20, `random_state=42`. | _à remplir_ |
| Technologie d'interface | Tkinter ; Streamlit ; Gradio | _volet 3, à décider_ | _à remplir_ |

