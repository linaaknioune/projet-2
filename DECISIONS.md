# Journal des décisions techniques

| Choix | Options envisagées | Choix retenu et justification | Validé par l'auxiliaire (date) |
|---|---|---|---|
| Domaine | Immobilier ; Transport ; Environnement et énergie | **Immobilier** : prédire le prix probable d'une maison. Domaine compréhensible par tous, pas de donnée sensible, un utilisateur peut tester des caractéristiques concrètes (qualité, surface, quartier, commerce à proximiter). |  23 octobre 2026 |
| Jeu de données | Kaggle : Prédiction de prix des maisons ; Kaggle : Données sur le transport de marchandises ; Kaggle : Données sur la fraude de carte de crédit | **Prédiction de prix des maisons, `train.csv`** 1 460 lignes (500 à 50 000 ✔), 79 colonnes d'entrée (≥ 5 ✔), variables numériques et catégorielles ✔, aucune donnée personnelle ✔, License: Kaggle ✔, cible `SalePrice` | à faire valider |
| Choix des variables d'entrée | Les 79 colonnes d'entrée ; sélection par corrélation ; sélection manuelle | **10 variables choisies à la main** (7 numériques : OverallQual, GrLivArea, TotalBsmtSF, GarageCars, YearBuilt, FullBath, LotArea ; 3 catégorielles : Neighborhood, KitchenQual, CentralAir). Une interface à 79 champs est inutilisable. | _à remplir_ |
| Nettoyage | Tout garder ; Retirer les valeurs aberrantes | **Retirer les valeurs aberrantes** Retirer les maisons de plus de 4000 pi² (recommandation de l'auteur du jeu), Retirer les doublons et les cibles invalides. Les valeurs manquantes sont imputées dans le pipeline (médiane / valeur la plus fréquente). | _à remplir_ |
| Cible et métrique | RMSE ; MAE ; R² | **Cible `SalePrice`, régression. Métrique principale : RMSE en dollars.** MAE et R² rapportés en complément| _à remplir_ |
| Modèle | Régression linéaire ; Forêt aléatoire ; K plus proches voisins | **Régression linéaire et forêt aléatoire comparées par validation croisée (5 blocs) sur l'entraînement seulement ; le meilleur est retenu.** | _à remplir_ |
| Séparation | a faire | a faire | _à remplir_ |
| Technologie d'interface | a faire | a decider | _à remplir_ |
