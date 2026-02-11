# Dockerfile pour le chargement des données (Exercice 2)
# ---------------------------------------------------
FROM python:3.11-slim

# Évite la génération de fichiers .pyc et assure un affichage direct des logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du script et des données
COPY load_data.py .
COPY csv_prepared/ ./csv_prepared/

# La base de données sera montée via un volume dans docker-compose
# pour persister les données sur l'hôte.

CMD ["python", "load_data.py"]
