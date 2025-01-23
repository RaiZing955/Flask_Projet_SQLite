from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction utilitaire pour vérifier si l'utilisateur est authentifié
def est_authentifie():
    return session.get('authentifie')

# Décorateur pour protéger les routes
def login_requis(f):
    def wrapper(*args, **kwargs):
        if not est_authentifie():
            return redirect(url_for('authentification'))  # Rediriger vers la page d'authentification
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__  # Garde le nom de la fonction originale
    return wrapper

# Fonction utilitaire pour récupérer les données de la base de données
def get_db_data(query, params=()):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

# Route pour la page d'accueil (authentification)
@app.route('/')
def hello_world():
    if est_authentifie():
        return redirect(url_for('index'))  # Si déjà authentifié, rediriger vers la page des livres
    return redirect(url_for('authentification'))  # Sinon, aller à la page d'authentification

# Route pour l'authentification
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  # Remplacer par une vérification sécurisée
            session['authentifie'] = True
            return redirect(url_for('index'))  # Rediriger vers la page des livres après authentification
        else:
            return render_template('formulaire_authentification.html', error=True)
    return render_template('formulaire_authentification.html', error=False)

# Route pour la déconnexion
@app.route('/deconnexion/')
def deconnexion():
    session.pop('authentifie', None)
    return redirect(url_for('hello_world'))  # Rediriger vers la page d'accueil après déconnexion

# Routes protégées (nécessitant une authentification)
@app.route('/index/')
@login_requis
def index():
    data = get_db_data('SELECT * FROM livres;')
    return render_template('index.html', data=data)

@app.route('/enregistrement/')
@login_requis
def enregistrement():
    data = get_db_data('SELECT * FROM livres;')
    return render_template('enregistrement_livre.html', data=data)

@app.route('/recherche/')
@login_requis
def recherche():
    data = get_db_data('SELECT * FROM livres WHERE quantite_disponible > 0;')
    return render_template('recherche_livre.html', data=data)

@app.route('/emprunt/')
@login_requis
def emprunt():
    data = get_db_data('SELECT * FROM emprunts;')
    return render_template('emprunt_livre.html', data=data)

@app.route('/gestion/')
@login_requis
def gestion_stocks():
    data = get_db_data('SELECT * FROM livres;')
    return render_template('gestion_stocks.html', data=data)

# Route pour afficher les clients (par exemple)
@app.route('/consultation/')
@login_requis
def consultation():
    data = get_db_data('SELECT * FROM clients;')
    return render_template('read_data.html', data=data)

# Route pour enregistrer un client
@app.route('/enregistrer_client', methods=['GET', 'POST'])
@login_requis
def enregistrer_client():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        adresse = request.form.get('adresse', 'Inconnu')
        query = 'INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)'
        params = (1002938, nom, prenom, adresse)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return redirect(url_for('consultation'))
    return render_template('formulaire.html')

# Route pour afficher la fiche d'un client
@app.route('/fiche_client/<int:post_id>/')
@login_requis
def fiche_client(post_id):
    data = get_db_data('SELECT * FROM clients WHERE id = ?', (post_id,))
    return render_template('read_data.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
