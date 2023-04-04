import requests
from flask import Flask, render_template, request, redirect
import psycopg2


app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
          user="postgres",
          password="Zundalar2245",
          host="localhost",
          port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute(
                "SELECT * FROM service.users WHERE login=%s AND password=%s",
                (str(username), str(password)))
            records = list(cursor.fetchall())
            if not records:
                return redirect("/registration/")
            return render_template('account.html', full_name=records[0][1], name=username, p=password)
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        print(login)
        cursor.execute(
            "SELECT id from service.users WHERE login='" + str(login) + "'")
        r = list(cursor.fetchall())
        print(r)
        if not (name and login and password) or r:
            return render_template('registration.html')
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()
        return redirect('/login/')
    return render_template('registration.html')


#http://localhost:5000/login/
