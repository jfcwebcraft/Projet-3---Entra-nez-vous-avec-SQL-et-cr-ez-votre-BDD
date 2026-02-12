# Exercice 3 - Analyse des Données avec SQL

## Objectif
Extraire et analyser les données immobilières du 1er semestre 2020 pour répondre aux besoins exprimés lors de la réunion de validation.

## Contexte
Suite à la création de la base de données et au chargement des données, nous devons maintenant répondre aux 12 besoins d'analyse identifiés lors de la réunion avec François Lapeyre (Directeur Général).

## Fichiers
- `requetes_analyse.sql` : Les 12 requêtes SQL répondant aux besoins
- `analyse_donnees.ipynb` : Notebook Jupyter avec exécution des requêtes et visualisations
- `support_presentation.md` : Support de présentation complet du projet

## Les 12 Besoins d'Analyse

### 1. Nombre total d'appartements vendus au 1er semestre 2020
- **Objectif** : Mesurer le volume total des ventes d'appartements
- **Période** : Janvier à juin 2020

### 2. Nombre de ventes d'appartement par région
- **Objectif** : Répartition géographique des ventes
- **Granularité** : Par région française

### 3. Proportion des ventes d'appartements par nombre de pièces
- **Objectif** : Préférences des acheteurs selon la taille
- **Analyse** : Répartition en pourcentages

### 4. Top 10 départements par prix du mètre carré
- **Objectif** : Identifier les zones les plus chères
- **Type** : Appartements uniquement

### 5. Prix moyen du mètre carré des maisons en Île-de-France
- **Objectif** : Valorisation du segment maisons en IDF
- **Zone** : Région Île-de-France uniquement

### 6. Top 10 appartements les plus chers
- **Objectif** : Analyse des biens premium
- **Informations** : Prix, surface, région, commune

### 7. Taux d'évolution des ventes Q1-Q2 2020
- **Objectif** : Mesurer la dynamique du marché
- **Calcul** : (Ventes_Q2 - Ventes_Q1) / Ventes_Q1 * 100

### 8. Classement régions par prix m² appartements >4 pièces
- **Objectif** : Analyse du segment haut de gamme
- **Filtre** : Appartements de plus de 4 pièces

### 9. Communes avec ≥50 ventes au 1er trimestre
- **Objectif** : Identifier les communes les plus actives
- **Seuil** : Minimum 50 transactions

### 10. Différence % prix m² 2 pièces vs 3 pièces
- **Objectif** : Analyser l'impact de la taille sur le prix
- **Comparaison** : Prix moyen 3 pièces / Prix moyen 2 pièces

### 11. Moyennes valeurs foncières top communes départements ciblés
- **Objectif** : Benchmark des meilleures communes
- **Départements** : 06, 13, 33, 59, 69
- **Classement** : Top 3 par département

### 12. Top 20 communes par transactions pour 1000 habitants
- **Objectif** : Mesurer l'activité relative
- **Filtre** : Communes > 10 000 habitants
- **Métrique** : Transactions / 1000 habitants

## Technologies Utilisées
- **SQL** : Requêtes complexes avec JOIN, CTE, fonctions d'agrégation
- **Python** : pandas, matplotlib, seaborn pour analyses et visualisations
- **Jupyter Notebook** : Interface interactive pour l'analyse

## Résultats Clés
- Base de données opérationnelle avec données du S1 2020
- 12 analyses complètes répondant aux besoins business
- Visualisations pour faciliter l'interprétation
- Recommandations stratégiques pour les agences

## Support de Présentation
Le fichier `support_presentation.md` contient :
- Contexte et objectifs du projet
- Démarche méthodologique complète
- Résultats des 12 analyses
- Recommandations stratégiques
- Perspectives d'évolution

## Comment Utiliser
1. Ouvrir `analyse_donnees.ipynb` dans Jupyter
2. Exécuter les cellules pour voir les résultats
3. Consulter `requetes_analyse.sql` pour les requêtes détaillées
4. Utiliser `support_presentation.md` pour la présentation

## Prochaines Étapes
- Validation du POC par la direction
- Extension aux données 2020 complètes
- Développement d'un dashboard interactif