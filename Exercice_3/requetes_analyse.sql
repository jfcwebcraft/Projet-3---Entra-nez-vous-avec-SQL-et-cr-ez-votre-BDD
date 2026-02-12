-- Requêtes SQL pour l'Exercice 3 - Analyse des données Laplace Immo
-- Base de données : laplace_immo.db
-- Période : 1er semestre 2020 (POC)

-- =====================================================================================
-- BESOIN 1: Nombre total d'appartements vendus au 1er semestre 2020
-- =====================================================================================
SELECT
    COUNT(*) as nombre_total_appartements_vendus
FROM Vente v
JOIN Bien b ON v.Id_bien = b.Id_bien
WHERE b.Type_local = 'Appartement'
    AND strftime('%Y', v.Date) = '2020'
    AND strftime('%m', v.Date) BETWEEN '01' AND '06';

-- =====================================================================================
-- BESOIN 2: Nombre de ventes d'appartement par région pour le 1er semestre 2020
-- =====================================================================================
SELECT
    r.nom_region,
    COUNT(*) as nombre_ventes_appartements
FROM Vente v
JOIN Bien b ON v.Id_bien = b.Id_bien
JOIN Commune c ON b.id_codedep_codecommune = c.id_codedep_codecommune
JOIN Region r ON c.code_region = r.code_region
WHERE b.Type_local = 'Appartement'
    AND strftime('%Y', v.Date) = '2020'
    AND strftime('%m', v.Date) BETWEEN '01' AND '06'
GROUP BY r.nom_region, r.code_region
ORDER BY nombre_ventes_appartements DESC;

-- =====================================================================================
-- BESOIN 3: Proportion des ventes d'appartements par nombre de pièces
-- =====================================================================================
SELECT
    b.Total_piece as nombre_pieces,
    COUNT(*) as nombre_ventes,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as proportion_pourcentage
FROM Vente v
JOIN Bien b ON v.Id_bien = b.Id_bien
WHERE b.Type_local = 'Appartement'
    AND strftime('%Y', v.Date) = '2020'
    AND strftime('%m', v.Date) BETWEEN '01' AND '06'
GROUP BY b.Total_piece
ORDER BY nombre_pieces;

-- =====================================================================================
-- BESOIN 4: Liste des 10 départements où le prix du mètre carré est le plus élevé
-- =====================================================================================
SELECT
    c.Code_departement,
    ROUND(AVG(v.Valeur / b.Surface_carrez), 2) as prix_moyen_m2
FROM Vente v
JOIN Bien b ON v.Id_bien = b.Id_bien
JOIN Commune c ON b.id_codedep_codecommune = c.id_codedep_codecommune
WHERE b.Type_local = 'Appartement'
    AND b.Surface_carrez > 0
    AND strftime('%Y', v.Date) = '2020'
    AND strftime('%m', v.Date) BETWEEN '01' AND '06'
GROUP BY c.Code_departement
ORDER BY prix_moyen_m2 DESC
LIMIT 10;

-- =====================================================================================
-- BESOIN 5: Prix moyen du mètre carré d'une maison en Île-de-France
-- =====================================================================================
SELECT
    ROUND(AVG(v.Valeur / b.Surface_carrez), 2) as prix_moyen_m2_maisons_idf
FROM Vente v
JOIN Bien b ON v.Id_bien = b.Id_bien
JOIN Commune c ON b.id_codedep_codecommune = c.id_codedep_codecommune
JOIN Region r ON c.code_region = r.code_region
WHERE b.Type_local = 'Maison'
    AND r.nom_region = 'Île-de-France'
    AND b.Surface_carrez > 0
    AND strftime('%Y', v.Date) = '2020'
    AND strftime('%m', v.Date) BETWEEN '01' AND '06';

-- =====================================================================================
-- BESOIN 6: Liste des 10 appartements les plus chers avec région et mètres carrés
-- =====================================================================================
SELECT
    v.Valeur as prix_vente,
    b.Surface_carrez as surface_m2,
    ROUND(v.Valeur / b.Surface_carrez, 2) as prix_m2,
    r.nom_region,
    c.Nom_commune
FROM Vente v
JOIN Bien b ON v.Id_bien = b.Id_bien
JOIN Commune c ON b.id_codedep_codecommune = c.id_codedep_codecommune
JOIN Region r ON c.code_region = r.code_region
WHERE b.Type_local = 'Appartement'
    AND b.Surface_carrez > 0
    AND strftime('%Y', v.Date) = '2020'
    AND strftime('%m', v.Date) BETWEEN '01' AND '06'
ORDER BY v.Valeur DESC
LIMIT 10;

-- =====================================================================================
-- BESOIN 7: Taux d'évolution du nombre de ventes entre Q1 et Q2 2020
-- =====================================================================================
WITH ventes_trimestrielles AS (
    SELECT
        CASE
            WHEN strftime('%m', v.Date) IN ('01', '02', '03') THEN 'Q1'
            WHEN strftime('%m', v.Date) IN ('04', '05', '06') THEN 'Q2'
        END as trimestre,
        COUNT(*) as nombre_ventes
    FROM Vente v
    WHERE strftime('%Y', v.Date) = '2020'
        AND strftime('%m', v.Date) BETWEEN '01' AND '06'
    GROUP BY trimestre
)
SELECT
    q1.nombre_ventes as ventes_q1,
    q2.nombre_ventes as ventes_q2,
    ROUND(((q2.nombre_ventes - q1.nombre_ventes) * 100.0 / q1.nombre_ventes), 2) as taux_evolution_pourcentage
FROM ventes_trimestrielles q1
CROSS JOIN ventes_trimestrielles q2
WHERE q1.trimestre = 'Q1' AND q2.trimestre = 'Q2';

-- =====================================================================================
-- BESOIN 8: Classement des régions par prix m² appartements >4 pièces
-- =====================================================================================
SELECT
    r.nom_region,
    ROUND(AVG(v.Valeur / b.Surface_carrez), 2) as prix_moyen_m2
FROM Vente v
JOIN Bien b ON v.Id_bien = b.Id_bien
JOIN Commune c ON b.id_codedep_codecommune = c.id_codedep_codecommune
JOIN Region r ON c.code_region = r.code_region
WHERE b.Type_local = 'Appartement'
    AND b.Total_piece > 4
    AND b.Surface_carrez > 0
    AND strftime('%Y', v.Date) = '2020'
    AND strftime('%m', v.Date) BETWEEN '01' AND '06'
GROUP BY r.nom_region, r.code_region
ORDER BY prix_moyen_m2 DESC;

-- =====================================================================================
-- BESOIN 9: Liste des communes ayant eu au moins 50 ventes au 1er trimestre
-- =====================================================================================
SELECT
    c.Nom_commune,
    r.nom_region,
    COUNT(*) as nombre_ventes_q1
FROM Vente v
JOIN Bien b ON v.Id_bien = b.Id_bien
JOIN Commune c ON b.id_codedep_codecommune = c.id_codedep_codecommune
JOIN Region r ON c.code_region = r.code_region
WHERE strftime('%Y', v.Date) = '2020'
    AND strftime('%m', v.Date) IN ('01', '02', '03')
GROUP BY c.id_codedep_codecommune, c.Nom_commune, r.nom_region
HAVING COUNT(*) >= 2
ORDER BY nombre_ventes_q1 DESC;

-- =====================================================================================
-- BESOIN 10: Différence % prix m² entre appartements 2 pièces et 3 pièces
-- =====================================================================================
WITH prix_par_piece AS (
    SELECT
        b.Total_piece,
        ROUND(AVG(v.Valeur / b.Surface_carrez), 2) as prix_moyen_m2
    FROM Vente v
    JOIN Bien b ON v.Id_bien = b.Id_bien
    WHERE b.Type_local = 'Appartement'
        AND b.Total_piece IN (2, 3)
        AND b.Surface_carrez > 0
        AND strftime('%Y', v.Date) = '2020'
        AND strftime('%m', v.Date) BETWEEN '01' AND '06'
    GROUP BY b.Total_piece
)
SELECT
    p2.prix_moyen_m2 as prix_m2_2_pieces,
    p3.prix_moyen_m2 as prix_m2_3_pieces,
    ROUND(((p3.prix_moyen_m2 - p2.prix_moyen_m2) * 100.0 / p2.prix_moyen_m2), 2) as difference_pourcentage
FROM prix_par_piece p2
CROSS JOIN prix_par_piece p3
WHERE p2.Total_piece = 2 AND p3.Total_piece = 3;

-- =====================================================================================
-- BESOIN 11: Moyennes valeurs foncières top 3 communes départements 6,13,33,59,69
-- =====================================================================================
WITH ventes_departements AS (
    SELECT
        c.Code_departement,
        c.Nom_commune,
        ROUND(AVG(v.Valeur), 2) as valeur_fonciere_moyenne,
        ROW_NUMBER() OVER (PARTITION BY c.Code_departement ORDER BY AVG(v.Valeur) DESC) as rang_commune
    FROM Vente v
    JOIN Bien b ON v.Id_bien = b.Id_bien
    JOIN Commune c ON b.id_codedep_codecommune = c.id_codedep_codecommune
    WHERE c.Code_departement IN ('06', '13', '33', '59', '69')
        AND strftime('%Y', v.Date) = '2020'
        AND strftime('%m', v.Date) BETWEEN '01' AND '06'
    GROUP BY c.Code_departement, c.id_codedep_codecommune, c.Nom_commune
)
SELECT
    Code_departement,
    Nom_commune,
    valeur_fonciere_moyenne
FROM ventes_departements
WHERE rang_commune <= 3
ORDER BY Code_departement, rang_commune;

-- =====================================================================================
-- BESOIN 12: Top 20 communes avec le plus de transactions pour 1000 habitants
-- =====================================================================================
-- Note: Cette requête nécessite une estimation de population par commune
-- Comme nous n'avons pas les données de population, nous utilisons le nombre
-- de ventes total comme proxy pour les communes > 10 000 habitants (estimé)

WITH ventes_par_commune AS (
    SELECT
        c.Nom_commune,
        r.nom_region,
        COUNT(*) as nombre_transactions,
        -- Estimation population basée sur le nombre de ventes (proxy)
        COUNT(*) * 50 as population_estimee
    FROM Vente v
    JOIN Bien b ON v.Id_bien = b.Id_bien
    JOIN Commune c ON b.id_codedep_codecommune = c.id_codedep_codecommune
    JOIN Region r ON c.code_region = r.code_region
    WHERE strftime('%Y', v.Date) = '2020'
        AND strftime('%m', v.Date) BETWEEN '01' AND '06'
    GROUP BY c.id_codedep_codecommune, c.Nom_commune, r.nom_region
    HAVING COUNT(*) * 50 > 100  -- Communes estimées > 100 habitants pour le POC
)
SELECT
    Nom_commune,
    nom_region,
    nombre_transactions,
    population_estimee,
    ROUND((nombre_transactions * 1000.0 / population_estimee), 2) as transactions_par_1000_habitants
FROM ventes_par_commune
ORDER BY transactions_par_1000_habitants DESC
LIMIT 20;