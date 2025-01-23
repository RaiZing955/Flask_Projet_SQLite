import sqlite3

# Connexion à la base de données SQLite (elle sera créée si elle n'existe pas)
conn = sqlite3.connect('bibliotheque.db')
cursor = conn.cursor()

# Création de la table "livres" si elle n'existe pas déjà
cursor.execute('''
    CREATE TABLE IF NOT EXISTS livres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        auteur TEXT NOT NULL,
        genre TEXT NOT NULL,
        annee_publication INTEGER,
        disponible BOOLEAN DEFAULT 1
    )
''')

# Liste des livres à insérer
livres = [
    ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Fiction', 1943),
    ('1984', 'George Orwell', 'Dystopie', 1949),
    ('Moby Dick', 'Herman Melville', 'Aventure', 1851),
    ('Les Misérables', 'Victor Hugo', 'Classique', 1862),
    ('Le Seigneur des Anneaux', 'J.R.R. Tolkien', 'Fantasy', 1954)
]

# Insertion des livres dans la table
cursor.executemany('''
    INSERT INTO livres (titre, auteur, genre, annee_publication) 
    VALUES (?, ?, ?, ?)
''', livres)

# Validation des changements et fermeture de la connexion
conn.commit()

# Affichage d'un message de succès
print("Livres ajoutés avec succès dans la base de données.")

# Fermeture de la connexion
conn.close()
