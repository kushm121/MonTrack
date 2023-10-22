import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, session
import cx_Oracle

app = Flask(__name__)
conn = cx_Oracle.connect('sys', 'dps123', 'localhost:1521/xe', cx_Oracle.SYSDBA)
cur = conn.cursor()
app.secret_key = "12345"



@app.route('/')
def index():
    return render_template('home.html')


@app.route('/loginform', methods=['POST'])
def loginform():
    username = request.form['username']
    password = request.form['password']
    cur.execute("select * from users where username = :username and password = :password",
                {'username': username, 'password': password})
    result = cur.fetchall()
    if result:
        session['username'] = username
        return redirect(f'/dashboard/{session["username"]}')
    else:
        message = "Invalid username or password"
        return render_template('practice.html', message=message)

#
# @app.route('/registerform', methods=['GET', 'POST'])
# def registerform():
#     username = request.form['username']
#     email = request.form['email']
#     password = request.form['password']
#     confirm_password = request.form['confirm_password']
#     date = datetime.date.today()
#
#     if username in ["deepan", "kushgra"]:
#         role = "admin"
#     else:
#         role = "user"
#
#     # Check if the username already exists
#     cur.execute("SELECT username FROM users WHERE username = :username", {'username': username})
#     existing_user = cur.fetchone()
#
#     if existing_user:
#         message = "Username already exists"
#         return render_template('signup.html', message=message)
#
#     # Check if passwords match
#     if password != confirm_password:
#         message = "Passwords do not match"
#         return render_template('signup.html', message=message)
#
#     try:
#         # Insert the new user into the database
#         print(username, email, password, role, date)
#         cur.execute(
#             "INSERT INTO users VALUES (:username, :password, :email, :role, SYSDATE)",
#             {'username': username, 'email': email, 'password': password, 'role': role})
#         conn.commit()
#         return redirect(url_for('loginform'))
#     except Exception as e:
#         # Handle database errors
#         print(str(e))  # Print the error for debugging purposes
#         conn.rollback()  # Rollback the transaction in case of error
#         message = "Registration failed. Please try again."
#         return render_template('signup.html', message=message)

@app.route('/registerform', methods=['POST'])
def registerform():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    date = datetime.date.today()
    if username in ["deepan", "kushgra"]:
        role = "admin"
    else:
        role = "user"
    usernames = cur.execute("select username from users")
    for i in usernames:
        if username == i[0]:
            message = "Username already exists"
            return render_template('signup.html', message=message)

    if password != confirm_password:
        message = "Passwords do not match"
        return render_template('signup.html', message=message)
    else:
        cur.execute(
            "INSERT INTO users VALUES (:username, :password, :email, :role, SYSDATE)",
            {'username': username, 'email': email, 'password': password, 'role': role})
        conn.commit()
        return render_template('practice.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('practice.html')


@app.route('/dashboard/<username>')
def dashboard(username):
    cur.execute("select username from users where username = :username", {'username': username})
    result = cur.fetchall()
    return render_template('index.html', result=result)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('practice.html')


if __name__ == '__main__':
    app.run(debug=True)

