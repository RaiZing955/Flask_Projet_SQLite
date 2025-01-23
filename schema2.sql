-- Table des utilisateurs
CREATE TABLE Utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Identifiant unique de l'utilisateur
    nom VARCHAR(100) NOT NULL,         -- Nom de l'utilisateur
    email VARCHAR(100) NOT NULL UNIQUE, -- Email unique
    mot_de_passe VARCHAR(255) NOT NULL, -- Mot de passe hashé
    role ENUM('Utilisateur', 'Administrateur') NOT NULL DEFAULT 'Utilisateur', -- Rôle de l'utilisateur
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Date d'inscription
);

-- Table des livres
CREATE TABLE Livres (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Identifiant unique du livre
    titre VARCHAR(255) NOT NULL,       -- Titre du livre
    auteur VARCHAR(255) NOT NULL,      -- Auteur du livre
    categorie VARCHAR(100),            -- Catégorie du livre
    quantite_totale INT NOT NULL CHECK (quantite_totale >= 0), -- Quantité totale en stock
    quantite_disponible INT NOT NULL CHECK (quantite_disponible >= 0), -- Quantité disponible
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Date d'ajout dans la bibliothèque
);

-- Table des prêts
CREATE TABLE Prets (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Identifiant unique du prêt
    utilisateur_id INT NOT NULL,       -- Référence à l'utilisateur
    livre_id INT NOT NULL,             -- Référence au livre
    date_emprunt TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date d'emprunt
    date_retour_prevue DATE NOT NULL,  -- Date de retour prévue
    date_retour_effective DATE,        -- Date réelle de retour
    statut ENUM('En cours', 'Terminé') DEFAULT 'En cours', -- Statut du prêt
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE, -- Clé étrangère pour utilisateur
    FOREIGN KEY (livre_id) REFERENCES Livres(id) ON DELETE CASCADE -- Clé étrangère pour livre
);

-- Table des stocks (historique des modifications de stock)
CREATE TABLE Stocks (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Identifiant unique de l'entrée de stock
    livre_id INT NOT NULL,             -- Référence au livre
    quantite_ajoutee INT NOT NULL,     -- Quantité ajoutée ou retirée (peut être négative)
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date de modification
    FOREIGN KEY (livre_id) REFERENCES Livres(id) ON DELETE CASCADE -- Clé étrangère pour livre
);

-- Vue pour les livres disponibles
CREATE VIEW LivresDisponibles AS
SELECT 
    id AS LivreID,
    titre AS Titre,
    auteur AS Auteur,
    categorie AS Categorie,
    quantite_disponible AS QuantiteDisponible
FROM Livres
WHERE quantite_disponible > 0;

-- Déclencheur pour mise à jour de la quantité disponible après un emprunt
DELIMITER $$
CREATE TRIGGER mise_a_jour_quantite_emprunt
AFTER INSERT ON Prets
FOR EACH ROW
BEGIN
    UPDATE Livres
    SET quantite_disponible = quantite_disponible - 1
    WHERE id = NEW.livre_id;
END$$
DELIMITER ;

-- Déclencheur pour mise à jour de la quantité disponible après un retour
DELIMITER $$
CREATE TRIGGER mise_a_jour_quantite_retour
AFTER UPDATE ON Prets
FOR EACH ROW
BEGIN
    IF NEW.statut = 'Terminé' THEN
        UPDATE Livres
        SET quantite_disponible = quantite_disponible + 1
        WHERE id = NEW.livre_id;
    END IF;
END$$
DELIMITER ;

-- Rapport statistique (par exemple : nombre de livres empruntés par utilisateur)
CREATE VIEW RapportStatistiques AS
SELECT 
    u.nom AS NomUtilisateur,
    COUNT(p.id) AS NombrePrets,
    MAX(p.date_emprunt) AS DernierEmprunt
FROM Prets p
JOIN Utilisateurs u ON p.utilisateur_id = u.id
GROUP BY u.nom;
