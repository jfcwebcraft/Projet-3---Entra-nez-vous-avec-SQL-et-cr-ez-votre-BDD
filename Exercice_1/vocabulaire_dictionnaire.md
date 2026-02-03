# Vocabulaire du Dictionnaire des Données

Ce document explique les termes techniques utilisés dans votre fichier `dictionnaire_donnees.csv`. Utile pour justifier vos choix à l'oral.

---

### 1. Les Types de Données (Standard SQL)

*   **INTEGER (INT)** : 
    *   *C'est quoi ?* Un nombre entier (sans virgule).
    *   *Exemple* : `Nombre_pieces_principales` (on ne peut pas avoir 3.5 pièces), `Code_postal`.
    
*   **VARCHAR** (Variable Character) : 
    *   *C'est quoi ?* Une chaîne de texte de longueur variable. C'est le standard pour stocker des mots.
    *   *Exemple* : `Nom_commune`, `Nature_culture`.
    *   *Pourquoi pas juste "TEXT" ?* `VARCHAR` permet souvent de limiter la taille (ex: VARCHAR(50)), ce qui optimise le stockage sur de grosses bases.

*   **FLOAT / DECIMAL** : 
    *   *C'est quoi ?* Un nombre à virgule (pour la précision).
    *   *Exemple* : `Surface_carrez` (ex: 45.55 m²), `Valeur_fonciere`.
    *   *Note* : `FLOAT` est approximatif (calcul scientifique), `DECIMAL` est exact (calcul financier).

*   **DATE** :
    *   *C'est quoi ?* Un format spécifique pour stocker l'année, le mois et le jour (AAAA-MM-JJ).
    *   *Avantage* : Permet d'utiliser des fonctions magiques comme `strftime` ou `YEAR()` pour extraire l'année facilement.

---

### 2. Les Clés (Constraints)

*   **PRIMARY KEY (PK) / Clé Primaire** :
    *   *Définition* : L'identifiant UNIQUE d'une ligne. C'est comme le numéro de sécurité sociale d'une donnée.
    *   *Exemple* : `Id_bien` est la PK de la table Bien. Il ne peut pas y avoir deux biens avec le même ID.

*   **FOREIGN KEY (FK) / Clé Étrangère** :
    *   *Définition* : Un lien vers une autre table. C'est le ciment de la base relationnelle.
    *   *Exemple* : Dans `Commune`, le champ `code_region` est une FK vers `Region`.
    *   *Sécurité* : Empêche de créer une commune dans une région qui n'existe pas.

---

### 3. Autres Termes

*   **NOT NULL** :
    *   *Définition* : Champ obligatoire. Interdit de laisser vide.
    *   *Exemple* : `Code_departement`. Une commune sans département, ça n'existe pas.

*   **Variable Atomique** :
    *   *Définition* : Une info indivisible.
    *   *Exemple* : Pas de colonne "Adresse_Complete", mais bien `Voie`, `Code_Postal`, `Ville` séparés.
