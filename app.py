from flask import Flask, request, redirect, flash, session
from flask.templating import render_template
import uuid

app = Flask(__name__, template_folder="static")
app.config['SECRET_KEY'] = str(uuid.uuid4())



@app.get("/")
def home():
    return render_template('home.html')


@app.get("/login")
def login():
    if session.get('user', None):
        return redirect(f"/users/{session['user']}")
    else:
        return render_template('login.html')
    


@app.get("/signup")
def signup():
    return render_template('signup.html')


@app.post("/signup")
def signup_post():
    import mysql.connector as mc
    import os
    passwd = os.getenv("DB_PASSWD_MYSQL")
    uname = request.form.get("uname")
    upassNew = request.form.get("passNew")
    upassCon = request.form.get("passCon")
    if upassNew != upassCon:
        flash("Passwords entered should match!")
        return redirect('/signup')
    if 8 > len(upassNew) or len(upassNew) > 16:
        flash("Passwords should be between 8 and 16 characters")
        return redirect('/signup')
    digit = alpha = False
    for val in upassNew:
        if val.isdigit():
            digit = True
        if val.isalpha():
            alpha = True
    if not (alpha and digit):
        flash("Passwords should be alphanumeric!")
        return redirect('/signup')
    try:
        with mc.connect(user="mydb_framebook", host="6ot.h.filess.io", passwd=passwd, port=3306) as obj:
            cursor = obj.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS mydb_framebook")
            cursor.execute("USE mydb_framebook")
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Data (UNo INT NOT NULL AUTO_INCREMENT PRIMARY KEY, UName VARCHAR(20) UNIQUE, UPass BINARY(128))")
            cursor.execute(f"SELECT * FROM Data WHERE UName='{uname}'")
            if cursor.fetchall():
                flash("This user already exists! Please try logging in!")
                return redirect('/login')
            else:
                cursor.execute(
                    f"INSERT INTO Data (UName, UPass) VALUES ('{uname}', AES_ENCRYPT('{upassNew}', 'key'))")
                obj.commit()
                return redirect('/login')

    except Exception as e:
        flash(f'{e}')
        return redirect('/error')


@app.post('/login')
def login_post():
    import mysql.connector as mc
    import os
    passwd = os.getenv("DB_PASSWD_MYSQL")
    uname = request.form.get("uname")
    upass = request.form.get("pass")
    try:
        with mc.connect(user="mydb_framebook", host="6ot.h.filess.io", passwd=passwd, database="mydb_framebook") as obj:
            cursor = obj.cursor()
            cursor.execute(f"SELECT IF(CAST(AES_ENCRYPT('{upass}', 'key') AS BINARY(128)) = UPass, '1', '0') FROM Data WHERE UName = '{uname}';")
            val = cursor.fetchone()
            if val is not None:
                if val[0] == '1':
                    session['user'] = uname
                    return redirect(f'/users/{uname}')
                else:
                    flash('Invalid Credentials !')
                    return redirect('/login')
            else:
                flash('Invalid Credentials !')
                return redirect('/login')
    except Exception as e:
        flash(f'{e}')
        return redirect('/error')

@app.get('/users/<uname>')
def users(uname):
    try:
        if session['user'] == uname:
            return render_template('dash.html', first_time=True)
        else:
            return redirect('/login')
    except:
        return redirect('/login')

@app.get('/logout')
def logout():
    if session.get('user', None):
        session.pop('user')
        return redirect('/login')
    else:
        return redirect('/login')

@app.post('/users/recommend')
def recommend():
    if session.get('user', None):
        import csv, random
        genre = request.form.get('inputGen')
        year = request.form.get('inputYr')
        with open("./data/data.csv", 'r', encoding="utf-8") as fin:
            csvr = csv.reader(fin)
            rec = []
            next(csvr)
            for row in csvr:
                if genre in row[3]:
                    if year == "new":
                        if int(row[4]) >= 2000:
                            rec.append(row)
                    elif year == "old":
                        if int(row[4]) < 2000:
                            rec.append(row)
                            
        recommended = rec[int(random.random()*(len(rec)-1))]
        title = recommended[1]
        link = f"https://open.spotify.com/search/{'%20'.join(title.split())}"
        return render_template('dash.html', recommended=recommended, link=link)
    else:
        return redirect('/login')

@app.get('/users/recommend')
def getRec():
    if session.get('user', None):
        return redirect(f"/users/{session.get('user')}")

@app.get('/error')
def error():
    return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=True)
