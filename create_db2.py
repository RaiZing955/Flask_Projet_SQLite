import sqlite3

def create_db():
    # Connexion à la base de données (si elle n'existe pas, elle sera créée)
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()

    # Création de la table des utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT CHECK(role IN ('utilisateur', 'administrateur')) NOT NULL
        )
    ''')

    # Création de la table des livres
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT NOT NULL,
            genre TEXT,
            disponible BOOLEAN NOT NULL DEFAULT 1,
            date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Création de la table des emprunts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprunts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER,
            id_livre INTEGER,
            date_emprunt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_retour TIMESTAMP,
            FOREIGN KEY(id_utilisateur) REFERENCES utilisateurs(id),
            FOREIGN KEY(id_livre) REFERENCES livres(id)
        )
    ''')

    # Création de la table des stocks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id_livre INTEGER,
            quantite INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(id_livre) REFERENCES livres(id)
        )
    ''')

    # Sauvegarder les changements et fermer la connexion
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    print("Base de données créée avec succès.")
