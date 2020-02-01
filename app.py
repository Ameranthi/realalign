from flask import Flask, request, jsonify, render_template, session
import mysql.connector
import os

sql_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="real_align"
)

app=Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/login', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor = sql_db.cursor()
        query =  'SELECT * FROM user where username =\'' + str(username) + '\' AND password = \'' + str(password) + '\''
        print (query)
        cursor.execute(query)
        result_sql = cursor.fetchall()
        print (result_sql)
        session['user'] = username
    return render_template('index.html') 

@app.route('/profile', methods=['POST', 'GET'])