# Guide Intermédiaire : La Méthode Merise pour votre Soutenance

Ce document vous donne les clés pour répondre à un examinateur qui creuserait la question de la méthodologie de conception.

---

### 1. La Philosophie
Merise est une méthode française (années 70) de conception de systèmes d'information. Son principe clé : **Séparer les données (QUOI) des traitements (COMMENT).**

Pour ce projet, nous nous sommes concentrés sur les **Données**.

---

### 2. Les 3 Niveaux de Modélisation (L'Argument Massue)

Si on vous demande "Comment avez-vous conçu votre base ?", répondez avec ces 3 étapes :

#### A. Le Niveau Conceptuel (MCD - Modèle Conceptuel de Données)
*   **C'est quoi ?** Le brouillon intelligent. On dessine des "Entités" (Vente, Bien) et des "Associations" (Concerne, Situe).
*   **Dans votre projet :**
    *   Vous avez identifié les Entités : `Bien`, `Commune`, `Region`, `Vente`.
    *   Vous avez défini les Cardinalités :
        *   Un Bien se situe dans **1 et 1 seule** Commune (1,1).
        *   Une Commune peut contenir **0 ou plusieurs** Biens (0,n).
    *   *L'argument clé :* "Au niveau conceptuel, une Vente ne concerne qu'un Bien, et un Bien est unique."

#### B. Le Niveau Logique (MLD - Modèle Logique de Données)
*   **C'est quoi ?** On traduit le dessin pour l'informatique relationnelle.
*   **La transformation clé (Règle d'or de Merise) :**
    *   "Toute association (1,n) se transforme en **Clé Étrangère**."
    *   *Exemple concret :* Comme un Bien est dans 1 seule Commune, j'ai pris l'identifiant de la Commune (`code_commune`) et je l'ai mis dans la table `Bien`. C'est devenu une FK (Foreign Key). C'est ça, la "migration de clé".
*   **C'est aussi là qu'on vérifie la 3NF :** On s'assure que chaque attribut dépend *uniquement* de la clé primaire.

#### C. Le Niveau Physique (MPD - Modèle Physique de Données)
*   **C'est quoi ?** Le code SQL réel.
*   **Dans votre projet :** C'est votre script Python qui fait les `CREATE TABLE` avec les types spécifiques à SQLite (`INTEGER`, `REAL`, `TEXT`).
*   *L'argument clé :* "Le MPD dépend du logiciel (SGBD). Ici c'est SQLite, mais si on passait sur PostgreSQL, seul le MPD changerait (les types), pas le MLD ni le MCD."

---

### 3. Résumé pour briller

> "Monsieur/Madame l'examinateur, ma démarche n'est pas empirique. J'ai suivi le cycle d'abstraction de Merise :
> 1.   **MCD** : J'ai d'abord listé mes objets métier (Dictionnaire des données).
> 2.  **MLD** : J'ai transformé ces relations en tables et clés étrangères (Schéma relationnel 3NF).
> 3.  **MPD** : J'ai implémenté cela techniquement dans SQLite via Python."
