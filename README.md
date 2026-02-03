# Projet 3 - Entraînez-vous avec SQL et créez votre BDD

Projet 3 du cursus DATA ENGINEERING OPENCLASSROOMS

## Contexte

Mission de Data Engineer chez Laplace Immo. Ce projet consiste à collecter et analyser l'ensemble des transactions immobilières en France (POC S1 2020) via une base de données relationnelle SQLite normalisée.

## Structure du projet (Normalisée)

```
├── Exercice_1/          # Modélisation & Dictionnaire
├── Exercice_2/          # ETL & Préparation des données (CSV)
├── Exercice_3/          # Analyses SQL & Soutenance
│   ├── requetes_analyse.sql     # Analyses SQL (SQLite)
│   ├── verifier_requetes.py     # Script de test automatisé
│   └── preparer_livrables.py    # Script de packaging final
├── laplace_immo.db      # Base de données SQLite principale
├── docker-compose.yml   # Explorateur de base de données Web
└── DOCKER_GUIDE.md      # Guide pour l'environnement Docker
```

## Technologies & Environnement

- **SGBD** : SQLite 3
- **Outils** : Docker Compose (Interface Web SQLite Explorer)
- **Langages** : SQL, Python 3.11 (pandas, logging)

## Installation & Utilisation

1. **Vérifier les analyses** :
   ```bash
   python "Exercice_3/verifier_requetes.py"
   ```

2. **Lancer l'explorateur web** (Optionnel) :
   ```bash
   docker compose up -d
   ```
   Accès sur : [http://localhost:8050](http://localhost:8050)

3. **Préparer les livrables** :
   ```bash
   python "Exercice_3/preparer_livrables.py"
   ```

## Conformité & Qualité
- **Normalisation** : Respect de la **3NF**.
- **Qualité de code** : Scripts Python documentés et structurés.
- **Simplicité** : Base SQLite portable et facile à explorer.
