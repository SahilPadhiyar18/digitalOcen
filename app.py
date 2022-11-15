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

@app.route('/', methods=['GET', 'POST']) #base root
def home_page():    
    return render_template('login.html')

@app.route('/validemail', methods=['POST','GET'])   #login
def validemail():
    try:
        if (request.method == 'POST'):
            name = (request.json['name'])
#             print(name)
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            conn
            cur = conn.cursor()
            sql = 'SELECT * FROM logindata WHERE email = %s;'
            cur.execute(sql,(name,))
            data = cur.fetchall()
            cur.close()
            conn.close()
            if(len(data) >= 1):
                return "&#10004;"
            else:
                return "&#10008"
    except:
        return "&#8263;"

@app.route('/signup', methods=['GET', 'POST']) #base root
def signup():    
    return render_template('signup.html')

@app.route('/loginpage', methods=['GET', 'POST']) #base root
def loginpage():    
    return render_template('login.html')

@app.route('/signUpSubmit', methods=['POST'])
def signUpSubmit():
    try:
        if request.method == "POST":    
            name = request.form.get("ck")  
            if(str(name) == "&#10004;"):
                add = request.form.get("fname")
                full_name = request.form.get("lname")
                emailaddr = request.form.get("email")
                passwordt = request.form.get("password")
                user = "user"
                mphone = request.form.get("phone")
                if(add == "s@hil" or add == "bhus@n"):
                    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                    conn
                    cur = conn.cursor()
                    cur.execute('INSERT INTO logindata (name, email,phone, password, addkey,logintype)'
                                'VALUES (%s, %s, %s, %s, %s, %s)',
                                (full_name,emailaddr,mphone,passwordt,add,user))
                    conn.commit()
                    cur.close()
                    conn.close() 
                    return render_template('login.html')
                else:
                    return render_template('signup.html')
            else:
                return render_template('signup.html')
    except:
#         print("step3")
        return render_template('signup.html')


@app.route('/cheakUserName', methods=['POST'])  #signup
def CheakUserName():
    try:
        if (request.method == 'POST'):
            name = (request.json['name'])
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            conn
            cur = conn.cursor()
            sql = 'SELECT * FROM logindata WHERE email = %s;'
            cur.execute(sql,(name,))
            data = cur.fetchall()
            cur.close()
            conn.close()
            if(len(data) == 1):
                return "&#10008;" #email exist
            else:
                return "&#10004;" #valid
    except:
        return "&#8263;"

@app.route('/LoginSubmit', methods=['POST'])
def logInSubmit():
    if request.method == "POST":      
        emailid = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("ck")
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#             conn
            cur = conn.cursor()
            sql = 'SELECT * FROM logindata WHERE email = %s;'
            cur.execute(sql,(emailid,))
            data = cur.fetchall()
            cur.close()
            conn.close()
            if(data[0][4]==password):
#                 print("passowed")
                # print("data[0][6]",data[0][6])
                if(data[0][6] == "admin"):
                    try:
                        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                        conn
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM roomdata;')
                        task = cur.fetchall()  
                        cur.close()
                        conn.close()
                        # print(task)    
                        task.sort()
                        return render_template('home.html' ,name = data[0][1],tasks=task[::-1])
                    except:
                        return render_template('home.html')
                elif(data[0][6] == "user"):
                    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                    cur = conn.cursor()
                    sql="SELECT rid FROM roomaccess where name= %s"
                    adr = (str(data[0][1]),)
                    cur.execute(sql,adr)
                    task = cur.fetchall()  
                    string = "SELECT * FROM roomdata where rid ='"
                    if(len(task)==1):
                        string += str(task[0][0])
                        string += "'"
                        cur.execute(string)
                        task = cur.fetchall()  
#                         print(string)
                        cur.close()
                        conn.close()
                        return render_template('user.html' ,name = data[0][1],tasks=task[::-1])
                    elif(len(task) > 1):
                        for i in range(len(task)-1):
                            string += str(task[i][0])
                            string += "'"
                            string += " or rid = '"
                        string += task[len(task)-1][0]
                        string += "'"
                        cur.execute(string)
                        task = cur.fetchall()  
#                         print(string)
                        cur.close()
                        conn.close()
                        task.sort()
#                         for i in task:
#                             print(i)
                        return render_template('user.html' ,name = data[0][1],tasks=task[::-1])
                    else:    
                        return render_template('user.html' ,name = data[0][1])
            else:
#                 print("encorrect pass")
                return render_template('login.html')
        except:
#             print("pass")
            return render_template('login.html')


@app.route('/espac', methods=['GET','POST'])
def espac():
    try:      
        name = str(request.args.get('name'))
        ac1c = str(request.args.get('ac1'))
        ac2c = str(request.args.get('ac2'))
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
#         print("name",name)
        sql = "SELECT * FROM roomdata WHERE rid = %s"
        var = (name, )
        cur.execute(sql,var)
        data = (cur.fetchall())
        if(len(data)<0):
            rpl = "name mismatch"
        else:
            rpl = str(data[0][4]) + str(data[0][7])
#             print("data",data)
            sql = "UPDATE roomdata SET ping = %s WHERE rid = %s"
            adr = (datetime.now(),name,)
            cur.execute(sql,adr)
            cur.execute('INSERT INTO currentdata (rid, ac1,ac2)'
                        'VALUES (%s, %s,%s)',
                        (name,ac1c, ac2c,))     
            conn.commit()
            cur.close()
            conn.close()
    except:
        rpl = "name mismatch"
    return str(rpl)

@app.route("/cheakbox", methods=['POST','GET'])
def cheakbox():
    swa = (request.json['sw'])
    stat = (request.json['data'])
    nam = (request.json['name'])
    x = swa.split("_")
    print(x[0],x[1])
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    s = "UPDATE roomdata SET "
    ql = "=%s WHERE id = %s"
    sql = s + str(x[1]) + ql 
    adr = (int(stat),int(x[0]),)
    cur.execute(sql, adr)
    # cur.execute('SELECT rid FROM roomdata where id = %s;',(int(x[0]),))
    # temp = cur.fetchall()
    # if(int(stat)==1):
    #     te = str(temp[0][0])+" "+str(x[1])+" is on"
    # else:
    #     te = str(temp[0][0])+" "+str(x[1])+" is off"
    # now = datetime.now()    
    # cur.execute('INSERT INTO logs (log, method, datetime)'    
    #             'VALUES (%s, %s, %s)',
    #             (te, nam,now,))

    # if(str(x[1])=="ac1" or str(x[1])=="ac2"):
    #     s = "UPDATE roomdata SET "
    #     ql = "=%s WHERE rid = %s"
    #     sql = s + str(x[1]) + ql 
    #     print(str(temp[0][0]))
    #     adr = (int(stat),str(temp[0][0]),)
    #     cur.execute(sql,adr)
    conn.commit()
    cur.close()
    conn.close()
    return "ok"



@app.route("/deleteRoom", methods=['POST','GET'])
def deleteRoom():
    rid = (request.json['rid'])
    name = (request.json['name'])
#     print(rid,name) 
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('DELETE FROM roomdata WHERE rid = %s',
                (rid,))
    conn.commit()
    cur.close()
    conn.close()
    return "ok"

@app.route('/addroom', methods=['POST','GET'])   #login
def addroom():
    return render_template('addroom.html')

@app.route('/addroomsubmit', methods=['POST'])   #login
def addroomsubmit():
    rid =    request.form.get("rid")    
    roomname =  request.form.get("roomname")
    ac1name =  request.form.get("ac1name")
    ac2name = request.form.get("ac2name")    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn
    cur = conn.cursor()

    cur.execute('INSERT INTO roomdata (rid, roomname, ac1name, ac1, lock1,ac2name, ac2, lock2)'
                            'VALUES (%s, %s,%s, %s, %s, %s,%s,%s)',
                            (rid,roomname,ac1name, 0,0,ac2name,0,0))

    # cur.execute('INSERT INTO roomdata (rid, espid, ac1, lock1, ac2, lock2)'
    #             'VALUES (%s, %s,%s, %s, %s, %s)',
    #             (rid, espid,0, 0,0,0))

    # cur.execute('INSERT INTO roomstatus (rid, espid, ac1, ac2)'
    #             'VALUES (%s, %s,%s, %s)',
    #             (rid, espid,0, 0))    
    conn.commit()
    cur.close()
    conn.close()
    # print(rid , espid)
    # adminlogin()
    return redirect('/adminlogin')


@app.route('/adminlogin')
def adminlogin():
    # name = request.args.get('name')
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT * FROM roomdata;')
    task = cur.fetchall()  
    cur.close()
    conn.close()
    return render_template('home.html' , tasks=task[::-1])

@app.route("/home")
def home():
    return redirect('/adminlogin')

@app.route('/accesslist', methods=['POST','GET'])
def accesslist():
    name = request.form.get('fullname')
    print("name",name)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT name FROM logindata where logintype = %s;',("user",))
    namelist = cur.fetchall()
    cur.execute('SELECT * FROM roomaccess where name = %s;',(name,))
    data = cur.fetchall()
#     print(data)
    conn.commit()
    cur.close()
    conn.close()
    return render_template('access.html' , namelist = namelist[::-1] , chooesname = name , tasks=data[::-1])

@app.route('/accessasign', methods=['POST','GET'])   #login
def accessasign():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn
    cur = conn.cursor()
    cur.execute('SELECT name FROM logindata where logintype = %s;',("user",))
    name = cur.fetchall()
    cur.execute('SELECT rid FROM roomdata;')
    rid = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('accessasign.html',name=name,rid=rid)


@app.route('/accessasignsub', methods=['POST','GET'])   #login
def accessasignsub():
    name =    request.form.get("name")
    rid =  request.form.get("rid")
    hour = request.form.get("hour")
#     print(name,rid,hour)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn
    cur = conn.cursor()
    time = datetime.now()
    cur.execute('INSERT INTO roomaccess (name, rid,hour)'
                'VALUES (%s, %s,%s)',
                (name,rid,time))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/accesslist')

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
