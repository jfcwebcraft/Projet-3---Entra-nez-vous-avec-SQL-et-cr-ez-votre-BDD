# Exercice 2 - Création de la Base de Données et Chargement des Données

## Objectif

Préparer les fichiers CSV conformes au schéma relationnel et charger les données dans la base de données Laplace Immo.

## Fichiers

- `load_data.py` : Script Python pour charger les CSVs dans la base de données
- `csv_prepared/` : Dossier contenant les CSVs préparés
  - `regions.csv`
  - `communes.csv`
  - `biens.csv`
  - `ventes.csv`

## Données Chargées

- Régions: 8
- Communes: 15
- Biens: 105
- Ventes: 160

## Étapes Réalisées

1. Préparation des CSVs conformes au schéma (clés primaires, étrangères, pas de doublons)
2. Chargement des données dans la base créée avec `../Exercice 1/create_database.sql`
3. Vérification de l'intégrité des données

## Livrables

- Fichiers CSV préparés
- Base de données avec données chargées
- Script de chargement automatique
