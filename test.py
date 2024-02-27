from flask import Flask, request, redirect, render_template, session, flash
import mysql.connector
import os

secret_key = os.urandom(20)

app = Flask('__name__')
app.secret_key = secret_key

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '18122001Bd-',
    'database': 'jdr'
}
def get_mysql_connection():
    return mysql.connector.connect(**mysql_config)


@app.route('/')
def main():
    if 'username' in session:
            return render_template('index.html', username=session['username'])
    else:
          return render_template('index.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] #POST Du champ Username
        password = request.form['password'] #POST du champ Password
    
        conn = get_mysql_connection() #Setup Connexion à MySQL
        query = conn.cursor(dictionary=True) #Pointer qui permets de requetter la BDD

        query.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username,password)) #Requete qui va recupere User/PWD
        user = query.fetchone()

        query.close()
        conn.close()

        if user:
             session['username'] = user['username']
             flash('T''es co batard', success)
             return redirect('/')
        else:
             flash('Mot de passe OU User invalide', 'error')
             return redirect('/login')
    else:
        return render_template('login.html')
        
          
    

if __name__ == "__main__":
    app.run(debug=True)