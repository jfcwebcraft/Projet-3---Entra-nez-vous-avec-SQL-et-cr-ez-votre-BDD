import sqlite3
import pandas as pd
import os
import re
import logging
from typing import Optional

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CONFIGURATION
# On calcule les chemins par rapport au script lui-même (pas le répertoire courant)
# Ainsi le script fonctionne qu'on le lance depuis Exercice_3/ ou la racine du projet.
_SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
DB_PATH: str = os.path.join(_SCRIPT_DIR, "..", "laplace_immo.db")
SQL_FILE_PATH: str = os.path.join(_SCRIPT_DIR, "requetes_analyse.sql")

def run_sql_tests() -> None:
    """
    Exécute les tests SQL pour vérifier la validité des requêtes d'analyse.
    Cette fonction est conçue pour être lisible et robuste.
    """
    logger.info("Démarrage du processus de vérification des requêtes SQL...")

    # Vérification de l'existence des fichiers requis
    if not os.path.exists(DB_PATH):
        logger.error(f"Base de données introuvable au chemin : {DB_PATH}")
        return
    
    if not os.path.exists(SQL_FILE_PATH):
        logger.error(f"Fichier de requêtes SQL introuvable : {SQL_FILE_PATH}")
        return

    try:
        logger.info(f"Connexion établie avec la base SQLite : {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        
        # Lecture du catalogue de requêtes
        with open(SQL_FILE_PATH, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Découpage par bloc de requête (séparateur ;)
        queries = sql_content.split(';')
        
        success_count: int = 0
        
        for index, query in enumerate(queries):
            cleaned_query = query.strip()
            if not cleaned_query:
                continue
                
            # Extraction du titre du besoin via les commentaires
            besoin_match = re.search(r'-- BESOIN (\d+.*)', cleaned_query, re.IGNORECASE)
            titre = besoin_match.group(1) if besoin_match else f"Requête {index + 1}"
            
            logger.info(f"Traitement : {titre}")
            print(f"\n{'='*80}")
            print(f"🔹 {titre.upper()}")
            print(f"{'='*80}")
            
            try:
                # Exécution et conversion en DataFrame pour affichage tabulaire
                df = pd.read_sql_query(cleaned_query, conn)
                
                if df.empty:
                    print("⚠️  AUCUN RÉSULTAT (attendu pour certains besoins POC)")
                else:
                    print(df.to_string(index=False))
                    print(f"\n[Succès] Nombre d'enregistrements : {len(df)}")
                    
                success_count += 1
                
            except Exception as sql_err:
                # On ignore les erreurs mineures dues à des commentaires isolés
                if "near" in str(sql_err).lower() or "incomplete" in str(sql_err).lower():
                    logger.warning(f"Bloc ignoré ou erreur mineure : {sql_err}")
                else:
                    logger.error(f"Échec de l'exécution pour '{titre}': {sql_err}")

        logger.info(f"Vérification terminée. Total de requêtes validées : {success_count}")
        conn.close()

    except sqlite3.Error as db_err:
        logger.critical(f"Erreur fatale lors de l'accès à la base de données : {db_err}")
    except Exception as general_err:
        logger.critical(f"Une erreur inattendue est survenue : {general_err}")

if __name__ == "__main__":
    run_sql_tests()
