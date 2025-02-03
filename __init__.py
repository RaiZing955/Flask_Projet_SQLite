from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Dictionnaire des utilisateurs pour l'authentification
utilisateurs = {
    "admin": {"password": "admin123", "role": "Admin"},
    "user": {"password": "12345", "role": "User"}
}

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')
# Fonction pour vérifier si l'utilisateur est admin
def est_admin():
    return session.get('role') == 'Admin'

# Route principale redirigeant vers les pages spécifiques en fonction du rôle
@app.route('/')
def index():
    if not est_authentifie():  # Vérifier si l'utilisateur est authentifié
        return redirect(url_for('authentification'))

# Rediriger vers la page appropriée en fonction du rôle
    if est_admin():
        return redirect(url_for('admin_home'))
    else:
        return redirect(url_for('user_home'))

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
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

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

# Route pour l'authentification
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vérifier les identifiants
        if username in utilisateurs and utilisateurs[username]["password"] == password:
            session['authentifie'] = True
            session['role'] = utilisateurs[username]["role"]
            session['utilisateur_id'] = username
            return redirect(url_for('index'))  # Rediriger vers la page principale

        return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

# Route pour se déconnecter
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('authentification'))

# Route pour la page Admin
@app.route('/admin_home', methods=['GET', 'POST'])
def admin_home():
    if not est_authentifie() or not est_admin():
        return "<h2>Accès refusé : Vous devez être administrateur pour accéder à cette page.</h2>", 403

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Ajouter un livre
        if 'ajouter_livre' in request.form:
            titre = request.form['titre']
            auteur = request.form['auteur']
            annee = request.form['annee']
            quantite = request.form['quantite']
            cursor.execute('INSERT INTO Livres (Titre, Auteur, Annee_publication, Quantite) VALUES (?, ?, ?, ?)', 
                           (titre, auteur, annee, quantite))
            conn.commit()

        # Supprimer un livre
        if 'supprimer_livre' in request.form:
            livre_id = request.form['livre_id']
            cursor.execute('DELETE FROM Livres WHERE ID_livre = ?', (livre_id,))
            conn.commit()

        # Ajouter au stock
        if 'ajouter_stock' in request.form:
            livre_id = request.form['livre_id']
            quantite_ajoutee = request.form['quantite']
            cursor.execute('UPDATE Livres SET Quantite = Quantite + ? WHERE ID_livre = ?', (quantite_ajoutee, livre_id))
            conn.commit()

    cursor.execute('SELECT * FROM Livres')
    livres = cursor.fetchall()
    conn.close()

    return render_template('admin_home.html', livres=livres)

@app.route('/user_home', methods=['GET', 'POST'])
def user_home():
    if not est_authentifie() or est_admin():
        return "<h2>Accès refusé : Vous devez être utilisateur pour accéder à cette page.</h2>", 403

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Gestion des emprunts
    if request.method == 'POST':
        # Emprunter un livre
        if 'emprunter' in request.form:
            livre_id = request.form['livre_id']
            cursor.execute('SELECT Quantite FROM Livres WHERE ID_livre = ?', (livre_id,))
            livre = cursor.fetchone()
            if livre and livre[0] > 0:
                cursor.execute('UPDATE Livres SET Quantite = Quantite - 1 WHERE ID_livre = ?', (livre_id,))
                cursor.execute('INSERT INTO Emprunts (ID_utilisateur, ID_livre) VALUES (?, ?)', 
                               (session['utilisateur_id'], livre_id))
                conn.commit()

        # Retourner un livre
        if 'retourner' in request.form:
            emprunt_id = request.form['emprunt_id']
            cursor.execute('SELECT ID_livre FROM Emprunts WHERE ID_emprunt = ?', (emprunt_id,))
            emprunt = cursor.fetchone()
            if emprunt:
                cursor.execute('UPDATE Livres SET Quantite = Quantite + 1 WHERE ID_livre = ?', (emprunt[0],))
                cursor.execute('UPDATE Emprunts SET Statut = "Terminé", Date_retour = DATE("now") WHERE ID_emprunt = ?', 
                               (emprunt_id,))
                conn.commit()

    # Récupérer la liste des livres disponibles
    cursor.execute('SELECT * FROM Livres')
    livres = cursor.fetchall()

    # Récupérer les emprunts en cours de l'utilisateur
    cursor.execute('''
        SELECT E.ID_emprunt, L.Titre, L.Auteur, E.Date_emprunt, E.Statut
        FROM Emprunts E
        JOIN Livres L ON E.ID_livre = L.ID_livre
        WHERE E.ID_utilisateur = ? AND E.Statut = "Actif"
    ''', (session['utilisateur_id'],))
    emprunts = cursor.fetchall()

    conn.close()

    return render_template('user_home.html', livres=livres, emprunts=emprunts)


# Route pour afficher les emprunts (Admin uniquement)
@app.route('/emprunts', methods=['GET'])
def voir_emprunts():
    if not est_authentifie() or not est_admin():
        return "<h2>Accès refusé : Vous devez être administrateur pour voir les emprunts.</h2>", 403

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        SELECT E.ID_emprunt, E.ID_utilisateur, L.Titre, L.Auteur, E.Date_emprunt, E.Date_retour, E.Statut
        FROM Emprunts E
        JOIN Livres L ON E.ID_livre = L.ID_livre
        WHERE E.Statut != "Terminé"
    ''')
    emprunts = cursor.fetchall()
    conn.close()

    return render_template('emprunts.html', emprunts=emprunts)

@app.route('/livres', methods=['GET', 'POST'])
def gerer_livres():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Gérer la recherche
    livres = []
    if request.method == 'POST' and 'recherche' in request.form:
        recherche = request.form['recherche']
        cursor.execute("""
            SELECT * FROM Livres
            WHERE Titre LIKE ? OR Auteur LIKE ? OR CAST(Annee_publication AS TEXT) LIKE ?
        """, (f'%{recherche}%', f'%{recherche}%', f'%{recherche}%'))
        livres = cursor.fetchall()
    else:  # Par défaut, afficher tous les livres
        cursor.execute('SELECT * FROM Livres')
        livres = cursor.fetchall()

    # Récupérer les emprunts en cours pour l'utilisateur connecté
    cursor.execute("""
        SELECT E.ID_emprunt, L.Titre, L.Auteur, E.Date_emprunt, E.Statut
        FROM Emprunts E
        JOIN Livres L ON E.ID_livre = L.ID_livre
        WHERE E.ID_utilisateur = ? AND E.Statut = "Actif"
    """, (session['utilisateur_id'],))
    emprunts = cursor.fetchall()

    conn.close()

    return render_template('user_home.html', livres=livres, emprunts=emprunts)
    
if __name__ == "__main__":
  app.run(debug=True)
