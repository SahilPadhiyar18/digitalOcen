from flask import *
import mysql.connector

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    mydb = mysql.connector.connect(
    host="120.72.91.157",
    user="admsljin_admsljinstitutes",
    password="Adms@_#2022",
    database="admsljin_adms_database"
    )
    print(mydb)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM customers")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    return  render_template('home.html',name= "sahil" , data = myresult)
 
if __name__ == '__main__':
    
#     app.jinja_env.auto_reload = True
#     app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
