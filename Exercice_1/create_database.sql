-- Script SQL pour créer la base de données Laplace Immo
-- Basé sur le schéma relationnel normalisé en 3NF
-- Mis à jour avec table Région selon besoins analyse
-- Adapté pour SQLite

-- Table Région
CREATE TABLE IF NOT EXISTS Region (
    code_region VARCHAR(2) PRIMARY KEY,
    nom_region VARCHAR(50) NOT NULL
);

-- Table Commune
CREATE TABLE IF NOT EXISTS Commune (
    id_codedep_codecommune VARCHAR(10) PRIMARY KEY,
    Code_departement VARCHAR(3) NOT NULL,
    Code_commune INT NOT NULL,
    Code_postal INT,
    Nom_commune VARCHAR(50) NOT NULL,
    code_region VARCHAR(2) NOT NULL,
    FOREIGN KEY (code_region) REFERENCES Region(code_region)
);

-- Table Bien
CREATE TABLE IF NOT EXISTS Bien (
    Id_bien INTEGER PRIMARY KEY AUTOINCREMENT,
    id_codedep_codecommune VARCHAR(10) NOT NULL,
    No_voie INT,
    BTO VARCHAR(1),
    Type_voie VARCHAR(4),
    Voie VARCHAR(50),
    Total_piece INT,
    Surface_carrez FLOAT,
    Surface_local INT,
    Type_local VARCHAR(50),
    FOREIGN KEY (id_codedep_codecommune) REFERENCES Commune(id_codedep_codecommune)
);

-- Table Vente
CREATE TABLE IF NOT EXISTS Vente (
    Id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_bien INT NOT NULL,
    Date DATE NOT NULL,
    Valeur INT NOT NULL,
    FOREIGN KEY (Id_bien) REFERENCES Bien(Id_bien)
);

-- Index pour optimiser les requêtes
CREATE INDEX idx_region_code ON Region(code_region);
CREATE INDEX idx_commune_dep ON Commune(Code_departement);
CREATE INDEX idx_commune_region ON Commune(code_region);
CREATE INDEX idx_bien_commune ON Bien(id_codedep_codecommune);
CREATE INDEX idx_vente_date ON Vente(Date);
CREATE INDEX idx_vente_bien ON Vente(Id_bien);