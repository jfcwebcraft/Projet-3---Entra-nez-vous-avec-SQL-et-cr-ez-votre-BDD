# Dictionnaire des Données - Projet Laplace Immo

## Table : Région

| Code | Signification | Type | Longueur | Nature | Règle de Gestion | Règle de Calcul |
|------|---------------|------|----------|--------|------------------|-----------------|
| code_region | Code de la région | VARCHAR | 2 | Clé primaire | Code officiel INSEE, non nul | - |
| nom_region | Nom de la région | VARCHAR | 50 | Attribut | Nom officiel, non nul | - |

## Table : Commune

| Code | Signification | Type | Longueur | Nature | Règle de Gestion | Règle de Calcul |
|------|---------------|------|----------|--------|------------------|-----------------|
| id_codedep_codecommune | Identifiant de la commune (clé étrangère) | VARCHAR | 10 | Clé primaire | Non nul, unique | Concaténation de Code_departement et Code_commune |
| Code_departement | Code du département | VARCHAR | 3 | Attribut | Peut inclure lettres (ex: 2A, 2B), non nul | - |
| Code_commune | Code de la commune | INTEGER | - | Attribut | Nombre entier, non nul | - |
| Code_postal | Code postal | INTEGER | - | Attribut | Nombre entier à 5 chiffres | - |
| Nom_commune | Nom de la commune | VARCHAR | 50 | Attribut | Nom officiel, non nul | - |
| code_region | Code de la région (clé étrangère) | VARCHAR | 2 | Clé étrangère | Référence Région.code_region, non nul | - |

## Table : Bien

| Code | Signification | Type | Longueur | Nature | Règle de Gestion | Règle de Calcul |
|------|---------------|------|----------|--------|------------------|-----------------|
| Id_bien | Identifiant unique du bien | INTEGER | - | Clé primaire | Auto-incrémenté, non nul | - |
| id_codedep_codecommune | Identifiant de la commune (clé étrangère) | VARCHAR | 10 | Clé étrangère | Référence Commune.id_codedep_codecommune, non nul | Concaténation de Code_departement et Code_commune |
| No_voie | Numéro de voie | INTEGER | - | Attribut | Peut être nul si non applicable | - |
| BTO | Indicateur Bâtiment de Type Ordinaire | VARCHAR | 1 | Attribut | Valeurs possibles : 'O' ou autre | - |
| Type_voie | Type de voie (ex: RUE, AV) | VARCHAR | 4 | Attribut | Abréviation standard | - |
| Voie | Nom de la voie | VARCHAR | 50 | Attribut | Nom complet de la rue | - |
| Total_piece | Nombre total de pièces | INTEGER | - | Attribut | Nombre entier positif | - |
| Surface_carrez | Surface en mètres carrés (loi Carrez) | FLOAT | - | Attribut | Valeur décimale positive | - |
| Surface_local | Surface totale du local | INTEGER | - | Attribut | Valeur entière positive | - |
| Type_local | Type de local (Appartement, Maison, etc.) | VARCHAR | 50 | Attribut | Valeur textuelle descriptive | - |

## Table : Vente

| Code | Signification | Type | Longueur | Nature | Règle de Gestion | Règle de Calcul |
|------|---------------|------|----------|--------|------------------|-----------------|
| Id_vente | Identifiant unique de la vente | INTEGER | - | Clé primaire | Auto-incrémenté, non nul | - |
| Id_bien | Identifiant du bien vendu (clé étrangère) | INTEGER | - | Clé étrangère | Référence Bien.Id_bien, non nul | - |
| Date | Date de la vente | DATE | - | Attribut | Format YYYY-MM-DD, non nul | - |
| Valeur | Valeur de la vente en euros | INTEGER | - | Attribut | Valeur entière positive | - |

## Conformité RGPD et 3NF

- **RGPD** : Seules les données nécessaires pour l'analyse immobilière sont conservées. Aucune donnée personnelle sensible au-delà de l'adresse (nécessaire pour localisation).
- **3NF** : Les tables sont normalisées. Pas de dépendances transitives. Par exemple, l'adresse est décomposée en éléments atomiques, et les communes sont séparées pour éviter redondance.