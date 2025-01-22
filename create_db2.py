import sqlite3

# Connexion à la base de données
connection = sqlite3.connect('bibliotheque.db')

# Chargement du schéma SQL pour créer les tables
with open('schema2.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insertion de livres
cur.execute("INSERT INTO Livres (titre, auteur, categorie, quantite_totale, quantite_disponible) VALUES (?, ?, ?, ?, ?)",
            ('1984', 'George Orwell', 'Fiction', 10, 10))
cur.execute("INSERT INTO Livres (titre, auteur, categorie, quantite_totale, quantite_disponible) VALUES (?, ?, ?, ?, ?)",
            ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Conte', 5, 5))
cur.execute("INSERT INTO Livres (titre, auteur, categorie, quantite_totale, quantite_disponible) VALUES (?, ?, ?, ?, ?)",
            ('Python pour les débutants', 'John Doe', 'Informatique', 7, 7))
cur.execute("INSERT INTO Livres (titre, auteur, categorie, quantite_totale, quantite_disponible) VALUES (?, ?, ?, ?, ?)",
            ('L’Alchimiste', 'Paulo Coelho', 'Roman', 8, 8))
cur.execute("INSERT INTO Livres (titre, auteur, categorie, quantite_totale, quantite_disponible) VALUES (?, ?, ?, ?, ?)",
            ('La Vie secrète des arbres', 'Peter Wohlleben', 'Science', 6, 6))

# Insertion d'utilisateurs
cur.execute("INSERT INTO Utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)",
            ('Admin', 'admin@bibliotheque.com', 'admin123', 'Administrateur'))
cur.execute("INSERT INTO Utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)",
            ('Alice', 'alice@example.com', 'password1', 'Utilisateur'))
cur.execute("INSERT INTO Utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)",
            ('Bob', 'bob@example.com', 'password2', 'Utilisateur'))
cur.execute("INSERT INTO Utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)",
            ('Eve', 'eve@example.com', 'password3', 'Utilisateur'))
cur.execute("INSERT INTO Utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)",
            ('Charlie', 'charlie@example.com', 'password4', 'Utilisateur'))

# Insertion de prêts (optionnel)
cur.execute("INSERT INTO Prets (utilisateur_id, livre_id, date_retour_prevue) VALUES (?, ?, ?)",
            (2, 1, '2025-02-01'))
cur.execute("INSERT INTO Prets (utilisateur_id, livre_id, date_retour_prevue) VALUES (?, ?, ?)",
            (3, 2, '2025-02-05'))

# Enregistrement des changements et fermeture de la connexion
connection.commit()
connection.close()
