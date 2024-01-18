# app.py
import random
import csv
from flask import Flask, render_template
from flask_socketio import SocketIO
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

socketio = SocketIO(app, cors_allowed_origins="*")

# Load messages from CSV file on server start
def load_messages():
    try:
        with open('messages.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            messages = list(reader)
    except FileNotFoundError:
        messages = []
    return messages

messages = load_messages()

def save_messages():
    with open('messages.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'msg', 'sentiment', 'probability', 'timestamp']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(messages)

def get_sentiment_probability():
    sentiments = ['Positive', 'Neutral', 'Negative']
    return {
        'sentiment': random.choice(sentiments),
        'probability': round(random.uniform(0.5, 1.0), 2)
    }

@app.route('/')
def receive():
    global messages
    messages = load_messages()
    return render_template('receive.html', messages=messages)

@app.route('/send')
def send():
    return render_template('send.html')

@socketio.on('text', namespace='/chat')
def text(message):
    global messages
    # Check if the message content is not empty or just spaces
    if message['msg'].strip():
        sentiment_probability = get_sentiment_probability()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_message = {
            'id': len(messages) + 1,
            'msg': message['msg'],
            'sentiment': sentiment_probability['sentiment'],
            'probability': sentiment_probability['probability'],
            'timestamp': timestamp  # Add timestamp to the message
        }
        messages.append(new_message)
        socketio.emit('message', new_message, namespace='/chat')
        save_messages()  # Save messages to CSV after adding a new message


if __name__ == '__main__':
    socketio.run(app)