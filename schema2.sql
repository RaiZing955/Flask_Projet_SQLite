-- Création de la table des utilisateurs
CREATE TABLE utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('utilisateur', 'administrateur') NOT NULL
);

-- Création de la table des livres
CREATE TABLE livres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    auteur VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    disponible BOOLEAN NOT NULL DEFAULT TRUE,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Création de la table des emprunts
CREATE TABLE emprunts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT,
    id_livre INT,
    date_emprunt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_retour TIMESTAMP,
    FOREIGN KEY(id_utilisateur) REFERENCES utilisateurs(id),
    FOREIGN KEY(id_livre) REFERENCES livres(id)
);

-- Création de la table des stocks
CREATE TABLE stocks (
    id_livre INT,
    quantite INT NOT NULL DEFAULT 0,
    FOREIGN KEY(id_livre) REFERENCES livres(id)
);
