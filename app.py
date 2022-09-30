from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello sahil'

@app.route('/sahil', methods=['GET','POST'])
def online():
    try:
        return "hello sahil"        
    except:
        return "data is not come"

if __name__ == '__main__':
    app.run()
