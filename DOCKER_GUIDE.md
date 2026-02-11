# Guide Docker - Environnement SQLite

Ce projet utilise Docker pour fournir une interface web conviviale permettant d'explorer la base de données SQLite du projet sans avoir à installer d'outils locaux (DBeaver, DB Browser, etc.).

## 🚀 Lancement rapide

1. **Démarrer l'environnement** :
   ```bash
   docker compose up -d
   ```

2. **Accéder à l'explorateur** :
   Ouvrez votre navigateur sur : **[http://localhost:8050](http://localhost:8050)**

## 📊 Fonctionnalités

Une fois l'interface `sqlite-web` ouverte, vous pouvez :
- **Explorer les tables** : `Bien`, `Commune`, `Region`, `Vente`.
- **Exécuter du SQL** : Allez dans l'onglet **"Query"** pour tester les requêtes d'analyse.
- **Visualiser les données** : Cliquez sur une table puis sur l'onglet **"Content"**.

## ⚙️ Détails Techniques

- **Image** : `coleifer/sqlite-web`
- **Base de données** : `laplace_immo.db` (liée directement au fichier local du projet).
- **Port** : `8050`

## 🛠️ Commandes utiles

- **Arrêter l'environnement** : `docker compose down`
- **Voir les logs** : `docker compose logs -f`
