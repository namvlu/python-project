from flask import Flask, render_template, request, redirect, url_for, make_response
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# Database configuration
DATABASE_CONFIG = {
    'dbname': 'dbtest',
    'user': 'postgres',
    'password': '123456',
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
#         user = cur.fetchone()
#         cur.close()
#         conn.close()
#         if user:
#             session['user_id'] = user[0]
#             return redirect(url_for('index'))
#         else:
#             return render_template('login.html', error="Sai tên đăng nhập hoặc mật khẩu.")
#     return render_template('login.html')

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM sinhvien')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', data=data)
#
# POST Request: When a form is submitted, the selected values are stored in a cookie.
# GET Request: On subsequent requests, the cookie's value is retrieved and used to query the database for the selected data.
@app.route('/details', methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        selected_data = request.form.getlist('selected')
        resp = make_response(redirect(url_for('details')))
        #Cookies: Used to store the selected MSSV values from the main page
        resp.set_cookie('selected_data', ','.join(selected_data))
        return resp
    # Cookie Retrieval: Reads the selected MSSV values from the cookie.
    selected_data = request.cookies.get('selected_data', '').split(',')
    if selected_data == ['']:
        selected_data = []

    conn = get_db_connection()
    cur = conn.cursor()
    if selected_data:
        query = sql.SQL("SELECT * FROM sinhvien WHERE mssv IN ({})").format(
            sql.SQL(', ').join(map(sql.Literal, selected_data))
        )
        cur.execute(query)
        data = cur.fetchall()
    else:
        data = []
    cur.close()
    conn.close()

    return render_template('details.html', data=data)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        mssv = request.form['mssv']
        ho_ten = request.form['ho_ten']
        tuoi = request.form['tuoi']
        dia_chi = request.form['dia_chi']
        que_quan = request.form['que_quan']
        chuyen_nganh = request.form['chuyen_nganh']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO sinhvien (mssv, ho_ten, tuoi, dia_chi, que_quan, chuyen_nganh) VALUES (%s, %s, %s, %s, %s, %s)", (mssv, ho_ten, tuoi, dia_chi, que_quan, chuyen_nganh))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('insert.html')

@app.route('/delete/<mssv>', methods=['POST'])
def delete(mssv):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM sinhvien WHERE mssv = %s", (mssv))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)