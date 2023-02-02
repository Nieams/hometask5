import requests
from flask import Flask, render_template, request
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

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if "" in [username, password]:
        error_str = "Одно из полей пустое"
        return render_template('error_page.html', error=error_str)
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if not records:
        error_str = "Пользователя нет в БД"
        return render_template('error_page.html', error=error_str)
    return render_template('account.html', full_name=records[0][1], username=records[0][2], password=records[0][3])
#http://localhost:5000/login/
