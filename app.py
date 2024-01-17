# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def receive():
    return render_template('receive.html')

@app.route('/send')
def send():
    return render_template('send.html')

@socketio.on('text', namespace='/chat')
def text(message):
    socketio.emit('message', {'msg': message['msg']}, namespace='/chat')

if __name__ == '__main__':
    socketio.run(app)
