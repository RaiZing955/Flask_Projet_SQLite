import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Charger un fichier SQL supplémentaire
    with open('schema2.sql') as f:
        conn.executescript(f.read())

    # Table des livres
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        available INTEGER NOT NULL DEFAULT 1,
        stock INTEGER NOT NULL
    )''')

    # Table des utilisateurs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        is_admin INTEGER DEFAULT 0
    )''')

    # Table des prêts
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS borrows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        borrow_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (book_id) REFERENCES books (id)
    )''')

    conn.commit()
    conn.close()

# Enregistrement d'un livre
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    stock = data.get('stock')

    if not all([title, author, stock]):
        return jsonify({"error": "Invalid input"}), 400

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author, stock, available) VALUES (?, ?, ?, ?)', (title, author, stock, stock))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book added successfully"}), 201

# Suppression d'un livre
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book deleted successfully"}), 200

# Recherche de livres disponibles
@app.route('/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE available > 0')
    books = cursor.fetchall()
    conn.close()

    books_list = [{"id": book[0], "title": book[1], "author": book[2], "available": book[3], "stock": book[4]} for book in books]
    return jsonify(books_list), 200

# Emprunt d'un livre
@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Vérifier si le livre est disponible
    cursor.execute('SELECT available FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    if not book or book[0] <= 0:
        conn.close()
        return jsonify({"error": "Book not available"}), 400

    # Enregistrer le prêt
    cursor.execute('INSERT INTO borrows (user_id, book_id, borrow_date) VALUES (?, ?, DATE('now'))', (user_id, book_id))
    cursor.execute('UPDATE books SET available = available - 1 WHERE id = ?', (book_id,))

    conn.commit()
    conn.close()
    return jsonify({"message": "Book borrowed successfully"}), 200

# Gestion des utilisateurs
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    is_admin = data.get('is_admin', 0)

    if not all([name, email]):
        return jsonify({"error": "Invalid input"}), 400

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, is_admin) VALUES (?, ?, ?)', (name, email, is_admin))
    conn.commit()
    conn.close()
    return jsonify({"message": "User added successfully"}), 201

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
