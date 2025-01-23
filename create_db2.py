import sqlite3

# Connexion à la base de données SQLite (ou création si elle n'existe pas)
connection = sqlite3.connect('bibliotheque.db')

# Création de la base de données et des tables
with connection:
    connection.executescript("""
        -- Table des utilisateurs
        CREATE TABLE IF NOT EXISTS Utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            mot_de_passe TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Utilisateur', 'Administrateur')),
            date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Table des livres
        CREATE TABLE IF NOT EXISTS Livres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT NOT NULL,
            categorie TEXT,
            quantite_totale INTEGER NOT NULL CHECK (quantite_totale >= 0),
            quantite_disponible INTEGER NOT NULL CHECK (quantite_disponible >= 0),
            date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Table des prêts
        CREATE TABLE IF NOT EXISTS Prets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur_id INTEGER NOT NULL,
            livre_id INTEGER NOT NULL,
            date_emprunt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_retour_prevue DATE NOT NULL,
            date_retour_effective DATE,
            statut TEXT NOT NULL CHECK(statut IN ('En cours', 'Terminé')) DEFAULT 'En cours',
            FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE,
            FOREIGN KEY (livre_id) REFERENCES Livres(id) ON DELETE CASCADE
        );

        -- Table des stocks
        CREATE TABLE IF NOT EXISTS Stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livre_id INTEGER NOT NULL,
            quantite_ajoutee INTEGER NOT NULL,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (livre_id) REFERENCES Livres(id) ON DELETE CASCADE
        );

        -- Vue pour les livres disponibles
        CREATE VIEW IF NOT EXISTS LivresDisponibles AS
        SELECT 
            id AS LivreID,
            titre AS Titre,
            auteur AS Auteur,
            categorie AS Categorie,
            quantite_disponible AS QuantiteDisponible
        FROM Livres
        WHERE quantite_disponible > 0;

        -- Déclencheur pour mise à jour de la quantité disponible après un emprunt
        CREATE TRIGGER IF NOT EXISTS mise_a_jour_quantite_emprunt
        AFTER INSERT ON Prets
        FOR EACH ROW
        BEGIN
            UPDATE Livres
            SET quantite_disponible = quantite_disponible - 1
            WHERE id = NEW.livre_id;
        END;

        -- Déclencheur pour mise à jour de la quantité disponible après un retour
        CREATE TRIGGER IF NOT EXISTS mise_a_jour_quantite_retour
        AFTER UPDATE ON Prets
        FOR EACH ROW
        BEGIN
            IF NEW.statut = 'Terminé' THEN
                UPDATE Livres
                SET quantite_disponible = quantite_disponible + 1
                WHERE id = NEW.livre_id;
            END IF;
        END;
    """)

# Message de confirmation
print("Base de données créée avec succès et tables initialisées.")

# Insertion de données d'exemple
with connection:
    # Ajout d'utilisateurs
    connection.execute("INSERT INTO Utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)",
                        ('Admin', 'admin@bibliotheque.com', 'password123', 'Administrateur'))
    connection.execute("INSERT INTO Utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)",
                        ('John Doe', 'john.doe@example.com', 'password123', 'Utilisateur'))

    # Ajout de livres
    connection.execute("INSERT INTO Livres (titre, auteur, categorie, quantite_totale, quantite_disponible) VALUES (?, ?, ?, ?, ?)",
                        ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Fiction', 10, 10))
    connection.execute("INSERT INTO Livres (titre, auteur, categorie, quantite_totale, quantite_disponible) VALUES (?, ?, ?, ?, ?)",
                        ('1984', 'George Orwell', 'Dystopie', 5, 5))

    # Ajout d'un prêt d'exemple
    connection.execute("INSERT INTO Prets (utilisateur_id, livre_id, date_retour_prevue) VALUES (?, ?, ?)",
                        (2, 1, '2025-02-01'))

print("Données d'exemple insérées avec succès.")

# Fermer la connexion
connection.close()
