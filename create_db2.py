import sqlite3

# Connexion à la base de données (ou création si elle n'existe pas)
connection = sqlite3.connect('bibliotheque.db')

# Création des tables dans la base de données
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
            quantite_totale INTEGER NOT NULL CHECK(quantite_totale >= 0),
            quantite_disponible INTEGER NOT NULL CHECK(quantite_disponible >= 0),
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
    """)

# Message de confirmation
print("Base de données créée avec succès et tables initialisées.")

# Fermer la connexion
connection.close()
