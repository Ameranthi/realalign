from flask import Flask, request, jsonify, render_template, session, redirect
import mysql.connector
import os

sql_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="real_align"
)
cursor = sql_db.cursor()

app=Flask(__name__)
app.secret_key = os.urandom(24)
app.config["IMAGE_UPLOADS"] = "C:\\Users\\rahul\\Desktop\\realalign\\static"

@app.route('/login', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        query =  'SELECT * FROM user where username =\'' + str(username) + '\' AND password = \'' + str(password) + '\''
        # print (query)
        cursor.execute(query)
        result_sql = cursor.fetchall()[0]
        # print (result_sql)
        session['user'] = result_sql[0]
        return redirect('/profile')
    return render_template('login.html') 

@app.route('/profile', methods=['POST', 'GET'])
def my_profile():
    user_id = None
    try:
        user_id = session['user']
    except:
        return render_template('not_authorized.html')

    if user_id:
        # user_id = session['user']
        if request.method == 'GET':
            query = 'SELECT * FROM userprofile where user_id =' + str(user_id)
            cursor.execute(query)
            # print (query, "!!!!!!!!!!!!!11111")
            result_sql = cursor.fetchall()[0]
            print (result_sql)
            ctx = {'first_name': result_sql[2], 'last_name': result_sql[3], 'profile_picture': result_sql[4], 'bio': result_sql[5]}
            return render_template('profile.html', context=ctx)

        if request.method == 'POST':
            bio = request.form.get('bio', '')
            # print (request, request.files, "@@@@@@@@@@@@@@@@@@@")
            image = request.files.get('profile_picture', '')

            if image:
                path = app.config['IMAGE_UPLOADS'] + '\\' + str(user_id)
                image.save(path)
                query1 = 'update userprofile set profile_picture=\'' + str(user_id) + '\' where user_id = ' + str(user_id);
                cursor.execute(query1)

            if bio:
                query2 = 'update userprofile set bio=\'' + str(bio) + '\' where user_id = ' + str(user_id);
                cursor.execute(query2)
            return redirect('/profile')

            # file_path
            # query2 = 'update table userprofile set profile_picture=\'' + profile_picture '\' where user_id = ' user_id;

