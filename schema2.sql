-- Création de la base de données (optionnel si déjà existant)
CREATE DATABASE IF NOT EXISTS Bibliotheque;
USE Bibliotheque;

-- Table des utilisateurs
CREATE TABLE Utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    role ENUM('Utilisateur', 'Administrateur') DEFAULT 'Utilisateur',
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des livres
CREATE TABLE Livres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    auteur VARCHAR(255) NOT NULL,
    categorie VARCHAR(100),
    quantite_totale INT NOT NULL,
    quantite_disponible INT NOT NULL,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des prêts
CREATE TABLE Prets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    livre_id INT NOT NULL,
    date_emprunt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_retour_prevue DATE NOT NULL,
    date_retour_effective DATE NULL,
    statut ENUM('En cours', 'Terminé') DEFAULT 'En cours',
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (livre_id) REFERENCES Livres(id) ON DELETE CASCADE
);

-- Vue pour la recherche des livres disponibles
CREATE VIEW LivresDisponibles AS
SELECT 
    id AS LivreID,
    titre AS Titre,
    auteur AS Auteur,
    categorie AS Categorie,
    quantite_disponible AS QuantiteDisponible
FROM Livres
WHERE quantite_disponible > 0;

-- Déclencheur pour mettre à jour la quantité disponible lors d'un emprunt
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

-- Déclencheur pour mettre à jour la quantité disponible lors d'un retour
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

-- Données initiales pour tester
INSERT INTO Utilisateurs (nom, email, mot_de_passe, role) 
VALUES ('Admin', 'admin@bibliotheque.com', 'admin123', 'Administrateur');

INSERT INTO Livres (titre, auteur, categorie, quantite_totale, quantite_disponible)
VALUES
('1984', 'George Orwell', 'Fiction', 10, 10),
('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Conte', 5, 5),
('Python pour les débutants', 'John Doe', 'Informatique', 7, 7);
