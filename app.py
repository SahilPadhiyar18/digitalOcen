from flask import Flask, render_template, url_for, copy_current_request_context

app = Flask(__name__)

@app.route('/')
def index():
    return "sahil"


if __name__ == '__main__':
    socketio.run(app)
