from flask import Flask, request, redirect, render_template, session,flash, url_for
from utils.sql import dbJdr
from utils.log import log
import logging
import os
from requests_oauthlib import OAuth2Session
import time
import hashlib

secret_key = os.urandom(20)

app = Flask('__name__', template_folder="/var/www/html/jdr/templates", static_folder="/var/www/html/jdr/static")
app.secret_key = secret_key
database = dbJdr()

SPOTIFY_CLIENT_ID = 'ac31e7858f4644c9a4034f45f79139f3'
SPOTIFY_CLIENT_SECRET = '989af8ec69814a18abde348039340e45'
SPOTIFY_REDIRECT_URI = 'https://benigne.dev/jdr/callback'
SCOPE = 'user-library-read'

# OAuth2 endpoints
AUTHORIZATION_BASE_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
USER_INFO_URL = 'https://api.spotify.com/v1/me'

def get_mysql_connection():
    return database.get_connection()


@app.route('/')
def main():
    if 'username' in session:
        return render_template('index.html', username=session["username"])
    else:
        return redirect('login')


@app.route('/callback')
def callback():
    spotify = OAuth2Session(SPOTIFY_CLIENT_ID, redirect_uri=SPOTIFY_REDIRECT_URI, state=session.get('oauth_state'))
    token = spotify.fetch_token(TOKEN_URL, client_secret=SPOTIFY_CLIENT_SECRET, authorization_response=request.url)
    
    # Save the token in session for later use
    session['oauth_token'] = token
    
    # Use the token to fetch user info
    response = spotify.get(USER_INFO_URL)
    user_info = response.json()
    
    return f"Welcome, {user_info['display_name']}!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/jdr')
    if request.method == 'POST':
        if request.form['username'] == "" or request.form['password'] == "":
            flash('Mot de passe OU Nom d\'utilisateur invalide', 'error')
            return render_template('login.html')

        username = request.form['username'] #POST Du champ Username
        password = request.form['password'].encode('UTF-8') #POST du champ Password

        hash_object = hashlib.sha256(password)
        hashed_password = hash_object.hexdigest()
        user = database.execute('SELECT * FROM users WHERE username ="' + str(username) + '" AND password = "' + str(hashed_password) + '";') #Requete qui va recupere User/PWD

        if user:
            session['username'] = user[0]['username']
            return redirect('/jdr')
        else:
            flash('Mot de passe OU Nom d\'utilisateur invalide', 'error')
    if "new_username" in session:
        new_username = session["new_username"]
        session.pop("new_username")
        return render_template('login.html', new_username=new_username)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.form['new_username'] == "" or request.form['new_password'] == "":
            flash('Mot de passe OU Nom d\'utilisateur invalide', 'error')
            return render_template('signup.html')
        new_username = request.form['new_username']
        new_password = request.form['new_password'].encode('utf-8')
        #Test si user déjà existant
        existing_user = database.execute('SELECT * FROM users WHERE username ="' + str(new_username) + '" ;')


        if existing_user:
            flash('Utilisateur déjà Existant', 'error')
            return render_template("signup.html")
        else:
            hash_object = hashlib.sha256(new_password)
            hashed_password = hash_object.hexdigest()

            database.execute('INSERT INTO users (username, password) VALUES ("' + str(new_username) + '", "' + str(hashed_password) +  '");')
            flash('Compte créé')
            session["new_username"] = new_username
            return redirect('login')
    return render_template("signup.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if "username" in session:
        session.pop("username")
    return redirect('/jdr')

@app.route('/newfiche', methods=['GET','POST'])
def newfiche():
    session["username"] = "caca"
    if "username" in session:
        username = session["username"]
        spells = ['Prout', 'Prout Magique', 'Prout Cosmiqueue']
        return render_template("character_sheet.html", username=username, spells=spells)
    else:
        return redirect('/jdr/login')

@app.route('/updatefiche', methods=['POST'])
def updatefiche():
    pass


if __name__ == "__main__":
    app.run(debug=True)
