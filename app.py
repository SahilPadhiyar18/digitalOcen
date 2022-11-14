from re import S
from telnetlib import STATUS
from this import d
from click import password_option
from flask import redirect
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os
import psycopg2
DATABASE_URL = "postgresql://doadmin:AVNS_Zenizxlwr33GAuLRsBv@db-postgresql-nyc1-45617-do-user-12450016-0.b.db.ondigitalocean.com:25060/defaultdb?sslmode=require"

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST']) 
def data_page():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT name FROM logindata;')
    data = cur.fetchall()
    cur.execute('SELECT email FROM logindata;')
    data1 = cur.fetchall()
    cur.execute('SELECT password FROM logindata;')
    data2 = cur.fetchall()
    cur.execute('SELECT logintype FROM logindata;')
    data3 = cur.fetchall()   
    cur.close()
    conn.close()
    return render_template('logindata.html',data = data[::-1] , data1 = data1[::-1],status = data2[::-1],onby=data3[::-1])

if __name__ == '__main__':
    # with app.app_context():
        # db.create_all()
    # db.switch.drop()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
