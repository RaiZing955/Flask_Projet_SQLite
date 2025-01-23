from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

    # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route index après une authentification réussie
            return redirect(url_for('index'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/index')
def index():
    # Vérifier si l'utilisateur est authentifié
    if not est_authentifie():
        return redirect(url_for('authentification'))
    
    return render_template('index.html')  # Afficher la page d'accueil (index)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement

# Route de gestion des livres
@app.route('/gestion_livres', methods=['GET', 'POST'])
def gestion_livres():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    # Si c'est une requête POST, on ajoute un livre
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        genre = request.form['genre']

        # Connexion à la base de données pour ajouter le livre
        conn = sqlite3.connect('bibliotheque.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO livres (titre, auteur, genre) VALUES (?, ?, ?)', (titre, auteur, genre))
        conn.commit()
        conn.close()
        return redirect(url_for('gestion_livres'))

    # Affichage des livres existants
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres')
    livres = cursor.fetchall()
    conn.close()
    return render_template('gestion_livres.html', livres=livres)

# Route d'emprunt de livres
@app.route('/emprunt', methods=['GET', 'POST'])
def emprunt():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    if request.method == 'POST':
        livre_id = request.form['livre_id']
        utilisateur_id = request.form['utilisateur_id']

        # Connexion à la base de données pour enregistrer l'emprunt
        conn = sqlite3.connect('bibliotheque.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO emprunts (id_livre, id_utilisateur) VALUES (?, ?)', (livre_id, utilisateur_id))
        conn.commit()
        conn.close()
        return redirect(url_for('emprunt'))

    # Affichage des livres disponibles pour emprunt
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres WHERE disponible = 1')
    livres_disponibles = cursor.fetchall()
    conn.close()
    return render_template('emprunt.html', livres=livres_disponibles)

# Route de gestion des utilisateurs
@app.route('/gestion_utilisateurs', methods=['GET', 'POST'])
def gestion_utilisateurs():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        role = request.form['role']

        # Connexion à la base de données pour ajouter un utilisateur
        conn = sqlite3.connect('bibliotheque.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO utilisateurs (nom, email, role) VALUES (?, ?, ?)', (nom, email, role))
        conn.commit()
        conn.close()
        return redirect(url_for('gestion_utilisateurs'))

    # Affichage des utilisateurs existants
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM utilisateurs')
    utilisateurs = cursor.fetchall()
    conn.close()
    return render_template('gestion_utilisateurs.html', utilisateurs=utilisateurs)

# Route de gestion des stocks
@app.route('/gestion_stocks', methods=['GET', 'POST'])
def gestion_stocks():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    if request.method == 'POST':
        livre_id = request.form['livre_id']
        quantite = request.form['quantite']

        # Connexion à la base de données pour mettre à jour le stock
        conn = sqlite3.connect('bibliotheque.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO stocks (id_livre, quantite) VALUES (?, ?)', (livre_id, quantite))
        conn.commit()
        conn.close()
        return redirect(url_for('gestion_stocks'))

    # Affichage des stocks
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT livres.titre, stocks.quantite FROM livres JOIN stocks ON livres.id = stocks.id_livre')
    stocks = cursor.fetchall()
    conn.close()
    return render_template('gestion_stocks.html', stocks=stocks)

if __name__ == "__main__":
    app.run(debug=True)
