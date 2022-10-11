from flask import *
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
 
@app.route('/')
def hello_world():

    client = pymongo.MongoClient("mongodb+srv://sahil:meHta9662@cluster0.48pouov.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client.test
   
    mydb = client["mydatabase"]
    mycol = mydb["customers"]

    x = mycol.find_one()

    print(x)
    

    return  render_template('home.html',name= "sahil" , data = x)
 
if __name__ == '__main__':
    
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
