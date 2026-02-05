# Schéma Relationnel - Projet Laplace Immo

Le schéma relationnel est basé sur la 3ème forme normale (3NF) pour éviter les redondances et assurer l'intégrité des données. Mis à jour selon les besoins en analyse identifiés en réunion.

## Tables

- **Région** : Informations sur les régions françaises
- **Commune** : Informations sur les communes, liées à une région
- **Bien** : Détails des biens immobiliers
- **Vente** : Historique des transactions

## Diagramme du Schéma

```mermaid
erDiagram
    Region ||--o{ Commune : "1,N - Une région contient plusieurs communes"
    Commune ||--o{ Bien : "1,N - Une commune contient plusieurs biens"
    Bien ||--o{ Vente : "1,N - Un bien peut avoir plusieurs ventes"

    Region {
        code_region VARCHAR(2) PK
        nom_region VARCHAR(50)
    }

    Commune {
        id_codedep_codecommune VARCHAR(10) PK
        Code_departement VARCHAR(3)
        Code_commune INT
        Code_postal INT
        Nom_commune VARCHAR(50)
        code_region VARCHAR(2) FK
    }

    Bien {
        Id_bien INT PK
        id_codedep_codecommune VARCHAR(10) FK
        No_voie INT
        BTO VARCHAR(1)
        Type_voie VARCHAR(4)
        Voie VARCHAR(50)
        Total_piece INT
        Surface_carrez FLOAT
        Surface_local INT
        Type_local VARCHAR(50)
    }

    Vente {
        Id_vente INT PK
        Id_bien INT FK
        Date DATE
        Valeur INT
    }
```

## Explications

- **Région** : Nouvelle table ajoutée pour répondre aux besoins d'analyse par région (ex: ventes par région, prix par région).
- **Commune** : Liée à Région via code_region. Clé primaire composite maintenue.
- **Bien et Vente** : Inchangés, mais permettent les analyses requises.

Ce schéma couvre tous les besoins exprimés en réunion : analyses par région, département, commune, type de bien, etc.