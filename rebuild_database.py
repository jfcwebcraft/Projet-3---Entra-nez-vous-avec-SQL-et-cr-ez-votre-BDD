"""
rebuild_database.py — Script de reconstruction complète de la base SQLite
=========================================================================
Ce script est le point d'entrée unique pour (re)créer la base laplace_immo.db
proprement, depuis les données sources CSV. Il est conçu pour la démonstration.

UTILISATION : python rebuild_database.py
PRÉREQUIS   : pip install pandas
RÉSULTAT    : laplace_immo.db recréée à la racine du projet
"""

import sqlite3
import os
import logging
import pandas as pd
from typing import List, Tuple

# --- CONFIGURATION DU LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- CHEMINS DU PROJET ---
# On cherche les fichiers par rapport à l'emplacement de ce script
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
DB_PATH: str = os.path.join(BASE_DIR, "laplace_immo.db")
SQL_SCHEMA_PATH: str = os.path.join(BASE_DIR, "Exercice_1", "create_database.sql")
CSV_DIR: str = os.path.join(BASE_DIR, "Exercice_2", "csv_prepared")


def supprimer_base_existante() -> None:
    """
    Supprime la base SQLite existante pour repartir de zéro.
    C'est indispensable pour éviter les conflits d'index ou de données dupliquées.
    """
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        logger.info(f"Base existante supprimée : {DB_PATH}")
    else:
        logger.info("Aucune base existante à supprimer.")


def creer_schema(conn: sqlite3.Connection) -> None:
    """
    Lit le fichier SQL de création du schéma (Exercice 1) et l'exécute.
    Ce fichier définit les 4 tables : Region, Commune, Bien, Vente.
    """
    logger.info(f"Lecture du schéma SQL depuis : {SQL_SCHEMA_PATH}")

    if not os.path.exists(SQL_SCHEMA_PATH):
        raise FileNotFoundError(
            f"Fichier de schéma introuvable : {SQL_SCHEMA_PATH}"
        )

    with open(SQL_SCHEMA_PATH, "r", encoding="utf-8") as f:
        sql_schema = f.read()

    # Activation des clés étrangères (désactivées par défaut dans SQLite)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(sql_schema)
    logger.info("Schéma créé avec succès (4 tables + index).")


def charger_donnees_csv(conn: sqlite3.Connection) -> None:
    """
    Charge les 4 fichiers CSV dans la base dans le bon ordre.
    L'ordre est crucial pour respecter les contraintes de clés étrangères :
      1. Region     (pas de dépendance)
      2. Commune    (dépend de Region)
      3. Bien       (dépend de Commune)
      4. Vente      (dépend de Bien)
    """
    # Ordre d'import obligatoire (respect des FK)
    fichiers: List[Tuple[str, str]] = [
        ("regions.csv", "Region"),
        ("communes.csv", "Commune"),
        ("biens.csv", "Bien"),
        ("ventes.csv", "Vente"),
    ]

    for nom_fichier, nom_table in fichiers:
        chemin_csv = os.path.join(CSV_DIR, nom_fichier)

        if not os.path.exists(chemin_csv):
            logger.warning(f"CSV manquant (ignoré) : {chemin_csv}")
            continue

        logger.info(f"Chargement de '{nom_fichier}' → table '{nom_table}'...")
        df = pd.read_csv(chemin_csv)

        # if_exists='append' : on ajoute sans écraser le schéma existant
        df.to_sql(nom_table, conn, if_exists="append", index=False)
        logger.info(f"  → {len(df)} lignes insérées dans '{nom_table}'.")


def verifier_chargement(conn: sqlite3.Connection) -> bool:
    """
    Vérifie que les données ont bien été chargées en comptant les lignes.
    Retourne True si tout est conforme aux attentes du POC.
    """
    logger.info("--- Vérification du chargement ---")

    # Volumes attendus pour ce POC
    volumes_attendus: dict = {
        "Region": 8,
        "Commune": 15,
        "Bien": 105,
        "Vente": 160,
    }

    tout_ok = True
    for table, attendu in volumes_attendus.items():
        cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
        reel = cursor.fetchone()[0]
        statut = "✅" if reel == attendu else "⚠️"
        logger.info(f"  {statut} {table:10} : {reel} lignes (attendu : {attendu})")
        if reel != attendu:
            tout_ok = False

    return tout_ok


def verifier_integrite_referentielle(conn: sqlite3.Connection) -> None:
    """
    Vérifie qu'il n'y a pas de 'biens orphelins' (biens sans commune associée).
    Un résultat de 0 confirme l'intégrité des données.
    """
    logger.info("--- Vérification de l'intégrité référentielle ---")
    cursor = conn.execute("""
        SELECT COUNT(*) FROM Bien b
        LEFT JOIN Commune c ON b.id_codedep_codecommune = c.id_codedep_codecommune
        WHERE c.id_codedep_codecommune IS NULL
    """)
    orphelins = cursor.fetchone()[0]

    if orphelins == 0:
        logger.info("  ✅ Aucun bien orphelin détecté. Intégrité parfaite.")
    else:
        logger.warning(f"  ⚠️ {orphelins} biens orphelins détectés !")


def main() -> None:
    """
    Point d'entrée principal : orchestre la reconstruction complète.
    """
    logger.info("=" * 60)
    logger.info("RECONSTRUCTION DE LA BASE LAPLACE IMMO")
    logger.info("=" * 60)

    try:
        # Étape 1 : Repartir d'une base propre
        supprimer_base_existante()

        # Étape 2 : Créer la connexion et le schéma
        conn = sqlite3.connect(DB_PATH)
        logger.info(f"Nouvelle base créée : {DB_PATH}")
        creer_schema(conn)

        # Étape 3 : Charger les données
        charger_donnees_csv(conn)
        conn.commit()

        # Étape 4 : Valider le résultat
        verifier_chargement(conn)
        verifier_integrite_referentielle(conn)

        conn.close()

        logger.info("=" * 60)
        logger.info("✅ BASE PRÊTE POUR LA DÉMONSTRATION")
        logger.info(f"   Fichier : {DB_PATH}")
        logger.info("   Lancez ensuite : python Exercice_3/verifier_requetes.py")
        logger.info("=" * 60)

    except FileNotFoundError as e:
        logger.critical(f"Fichier requis introuvable : {e}")
    except sqlite3.Error as e:
        logger.critical(f"Erreur SQLite : {e}")
    except Exception as e:
        logger.critical(f"Erreur inattendue : {e}")
        raise


if __name__ == "__main__":
    main()
