# Exercice 1 - Compréhension des Données et Schéma Relationnel

## Objectif
Analyser les données fournies par Laplace Immo, créer le dictionnaire des données et concevoir le schéma relationnel de la base de données pour le projet.

## Livrables Principaux

- **`dictionnaire_donnees.md`** : Le dictionnaire des données complet (format Markdown) détaillant :
  - Les tables (Region, Commune, Bien, Vente)
  - Les colonnes avec leur type, longueur et nature
  - Les règles de gestion et contraintes (Clés primaires, étrangères)

- **`schema_relationnel.md`** : Documentation du schéma relationnel conçu, incluant :
  - La description des tables et relations
  - Le diagramme Entité-Association (Mermaid) respectant la 3ème forme normale (3NF)

- **`create_database.sql`** : Le script SQL DDL (Data Definition Language) résultant de la modélisation, permettant de créer la structure vide de la base de données.

## Fichiers Annexes
- `schema_relationnel_via_lucid_app.png` : Image du schéma relationnel réalisé avec Lucidchart.
- `analyse_donnees.ipynb` : Notebook d'exploration et de vérification de la base de données.
- `laplace_immo.db` : Fichier de la base de données SQLite (structure créée et données chargées).

## Méthodologie
1. **Analyse des besoins** : Identification des données nécessaires pour répondre aux questions business.
2. **Normalisation** : Conception d'un modèle respectant la 3NF pour éviter redondances et incohérences.
3. **Dictionnaire** : Formalisation des métadonnées.
4. **Implémentation** : Traduction du modèle théorique en script SQL.