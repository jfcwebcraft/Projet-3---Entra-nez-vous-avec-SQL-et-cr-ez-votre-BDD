import os
import shutil
import zipfile
import logging
import time
import stat
from datetime import datetime
from typing import List

# --- CONFIGURATION DU LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION DU PROJET ---
NOM: str = "CHAUSSOY"
PRENOM: str = "JEANFRANCOIS"
DATE_DEBUT: str = "012026" # MMYYYY
NOM_PROJET: str = "Projet_3_SQL"

# Calcul du répertoire racine du projet par rapport au script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def remove_readonly(func, path, excinfo):
    """Callback pour rmtree afin de forcer la suppression des fichiers en lecture seule sur Windows."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def robust_rmtree(path: str):
    """Supprime un dossier de manière robuste en gérant les délais Windows et les droits."""
    if not os.path.exists(path):
        return
        
    for i in range(3): # Tentatives de suppression (Windows peut être lent à libérer les locks)
        try:
            shutil.rmtree(path, onerror=remove_readonly)
            return
        except PermissionError:
            if i < 2:
                logger.warning(f"Accès refusé sur {path}, nouvelle tentative dans 1s... (Fermez vos dossiers ouverts !)")
                time.sleep(1)
            else:
                logger.error(f"Impossible de supprimer complètement {path}. Vérifiez qu'aucun fichier n'est ouvert.")

def cleanup_project() -> None:
    """
    Nettoie le projet en renommant les dossiers et en supprimant les fichiers inutiles.
    """
    logger.info("Vérification de la structure du projet...")
    
    renames = {
        "Exercice 1": "Exercice_1",
        "Exercice 2": "Exercice_2",
        "Exercice 3": "Exercice_3"
    }
    
    # On vérifie si on doit renommer (au cas où ce n'est pas déjà fait)
    for old_name, new_name in renames.items():
        old_path = os.path.join(BASE_DIR, old_name)
        new_path = os.path.join(BASE_DIR, new_name)
        
        if os.path.exists(old_path):
            try:
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    logger.info(f"Dossier renommé : {old_name} -> {new_name}")
            except Exception as e:
                logger.warning(f"Note : Impossible de renommer {old_name} (peut-être déjà fait ou ouvert) : {e}")

    # Suppression des fichiers résiduels
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if any(ext in file for ext in [".metadata.json", ".resolved"]):
                try:
                    os.remove(os.path.join(root, file))
                except Exception:
                    pass

def preparer_livrables() -> None:
    """
    Assemble les livrables finaux.
    """
    logger.info("Préparation du package final...")
    
    folder_name: str = f"{NOM_PROJET}_{NOM}_{PRENOM}"
    output_dir = os.path.join(BASE_DIR, folder_name)
    
    # Réinitialisation Robuste
    robust_rmtree(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Chemins sources standardisés
    ex1_dir = os.path.join(BASE_DIR, "Exercice_1")
    ex3_dir = os.path.join(BASE_DIR, "Exercice_3")

    # 1. Dictionnaire
    src_dict = os.path.join(ex1_dir, "dictionnaire_donnees.csv")
    dst_dict = os.path.join(output_dir, f"{NOM}_{PRENOM}_1_dictionnaire_{DATE_DEBUT}.csv")
    
    if os.path.exists(src_dict):
        shutil.copy(src_dict, dst_dict)
        logger.info(f"Livrable 1 (Dictionnaire) ajouté : {dst_dict}")
    else:
        logger.warning(f"Volume source manquant : {src_dict}")

    # 2. Support (PDF)
    src_pres = os.path.join(BASE_DIR, "Support_de_présentation_projet_3.pdf")
    dst_pres = os.path.join(output_dir, f"{NOM}_{PRENOM}_2_support_{DATE_DEBUT}.pdf")
    
    if os.path.exists(src_pres):
        shutil.copy(src_pres, dst_pres)
        logger.info(f"Livrable 2 (Support PDF) ajouté : {dst_pres}")
    else:
        logger.warning(f"Support PDF manquant : {src_pres}")

    # 3. Technique
    tech_folder = os.path.join(output_dir, "Technique_et_Soutenance")
    if not os.path.exists(tech_folder):
        os.makedirs(tech_folder)
    
    # Chemin vers les fichiers de soutenance (déplacés dans Docs/Soutenance/)
    soutenance_dir = os.path.join(BASE_DIR, "Docs", "Soutenance")

    files_to_copy = [
        # Livrables techniques officiels (Exercice 3)
        (ex3_dir, "requetes_analyse.sql"),
        (ex3_dir, "verifier_requetes.py"),
        (ex3_dir, "schema_relationnel.md"),
        # Fichiers de présentation et soutenance (Docs/Soutenance/)
        (soutenance_dir, "explications_sql_detaillees.md"),
        (soutenance_dir, "guide_pedagogique_detaille.md"),
        (soutenance_dir, "notes_presentation_sql.md"),
        (soutenance_dir, "notes_orales_soutenance.md"),
        (soutenance_dir, "guide_explication_requetes.md"),
        (soutenance_dir, "auto_evaluation_remplie.md"),
        # Infrastructure Docker
        (BASE_DIR, "DOCKER_GUIDE.md"),
        (BASE_DIR, "docker-compose.yml"),
        # Base de données SQLite
        (BASE_DIR, "laplace_immo.db")
    ]
    
    # Ajout du dossier Docs (Instructions d'origine)
    docs_src = os.path.join(BASE_DIR, "Docs")
    docs_dst = os.path.join(output_dir, "Docs")
    if os.path.exists(docs_src):
        shutil.copytree(docs_src, docs_dst)
        logger.info(f"Dossier Docs ajouté.")
    
    for folder, filename in files_to_copy:
        src = os.path.join(folder, filename)
        if os.path.exists(src):
            shutil.copy(src, tech_folder)
    
    # 4. ZIP
    zip_path = os.path.join(BASE_DIR, f"{folder_name}.zip")
    logger.info(f"Compression : {zip_path}")
    
    # On ferme l'ancien zip s'il existe
    if os.path.exists(zip_path):
        try: os.remove(zip_path)
        except Exception: pass

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            if folder_name in root: # On ne zippe que le contenu du dossier de sortie
                for file in files:
                    abs_p = os.path.join(root, file)
                    rel_p = os.path.relpath(abs_p, BASE_DIR)
                    zipf.write(abs_p, rel_p)
    
    logger.info("Traitement terminé.")
    logger.info(f"Archive prête pour dépôt : {os.path.abspath(zip_path)}")

if __name__ == "__main__":
    cleanup_project()
    preparer_livrables()
