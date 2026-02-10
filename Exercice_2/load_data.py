import pandas as pd
import sqlite3
import os
import logging
from typing import List

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def charger_donnees_exercice_2(db_path: str = '../laplace_immo.db', csv_dir: str = 'csv_prepared') -> None:
    """
    SCRIPT DE CHARGEMENT DES DONNÉES (Exercice 2)
    --------------------------------------------
    Ce script automatise l'importation des fichiers CSV préparés dans la base SQLite.
    Il respecte les contraintes de clés étrangères définies dans le schéma relationnel.
    """
    
    try:
        # 1. Vérification du fichier de base de données
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
        logger.info(f"Connexion à la base de données : {os.path.abspath(db_path)}")
        conn = sqlite3.connect(db_path)
        
        # 2. Définition des fichiers à charger
        fichiers = [
            ('regions.csv', 'Region'),
            ('communes.csv', 'Commune'),
            ('biens.csv', 'Bien'),
            ('ventes.csv', 'Vente')
        ]
        
        # 3.Chargement et Insertion
        for filename, table_name in fichiers:
            path = os.path.join(csv_dir, filename)
            if os.path.exists(path):
                logger.info(f"Chargement de {filename} dans la table {table_name}...")
                df = pd.read_csv(path)
                # On utilise 'append' pour ajouter aux données existantes (ou 'replace' pour repartir à zéro)
                df.to_sql(table_name, conn, if_exists='append', index=False)
            else:
                logger.warning(f"Fichier manquant : {path}")

        # 4. Vérification finale des volumes
        logger.info("Vérification des volumes de données chargés :")
        for _, table_name in fichiers:
            count = pd.read_sql(f'SELECT COUNT(*) FROM {table_name}', conn).iloc[0,0]
            logger.info(f"Table {table_name:10} : {count} lignes")

        logger.info("Importation terminée.")

    except Exception as e:
        logger.error(f"Erreur lors du chargement : {str(e)}")
        raise

if __name__ == "__main__":
    charger_donnees_exercice_2()