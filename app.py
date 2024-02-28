from flask import Flask, request, redirect, render_template, session,flash, url_for
from utils.sql import dbJdr
from fiche import *
import logging
import os
import time
import hashlib

secret_key = os.urandom(20)

app = Flask('__name__', template_folder="/var/www/html/jdr/templates")
app.secret_key = secret_key
database = dbJdr()

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '18122001Bd-',
    'database': 'jdr'
}
def get_mysql_connection():
    return database.get_connection()


@app.route('/')
def main():
    #app.logger.debug(url_for('static', filename='style.css'))
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/jdr')
    if request.method == 'POST':
        username = request.form['username'] #POST Du champ Username
        password = request.form['password'].encode('UTF-8') #POST du champ Password

        hash_object = hashlib.sha256(password)
        hashed_password = hash_object.hexdigest()
        user = database.execute('SELECT * FROM users WHERE username ="' + str(username) + '" AND password = "' + str(hashed_password) + '";') #Requete qui va recupere User/PWD

        if user:
            session['username'] = user[0]['username']
            flash('T''es co batard', 'success')
            return redirect('/jdr')
        else:
            flash('Mot de passe OU User invalide', 'error')
            time.sleep(3)
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password'].encode('utf-8')
        #Test si user déjà existant
        existing_user = database.execute('SELECT * FROM users WHERE username ="' + str(new_username) + '" ;')


        if existing_user:
            flash('User déjà Existant', 'error')
            return render_template("signup.html")
        else:
            hash_object = hashlib.sha256(new_password)
            hashed_password = hash_object.hexdigest()

            database.execute('INSERT INTO users (username, password) VALUES ("' + str(new_username) + '", "' + str(hashed_password) +  '");')
            flash('Compte crée')
            return render_template('login.html')
    return render_template("signup.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/jdr')

@app.route('/fiches')
def fiches():
    #return fiching(app)
    pass



if __name__ == "__main__":
    app.run(debug=True)
