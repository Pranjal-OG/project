from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
import sqlite3
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
socketio = SocketIO(app)

online_users = set()

# Create messages.db if not exists
if not os.path.exists('messages.db'):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender TEXT,
                        message TEXT,
                        timestamp TEXT
                    )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = {'pranjal': 'pranjal@2206', 'richa': 'richa@0622'}
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/chat')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect('/')
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sender, message FROM messages ORDER BY id ASC")
    messages = cursor.fetchall()
    conn.close()
    return render_template('chat.html',
                           username=session['username'],
                           messages=messages,
                           messages_tojson=json.dumps(messages))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@socketio.on('send_message')
def handle_send(data):
    timestamp = datetime.now().strftime('%H:%M')
    sender = session.get('username')
    message = data['message']
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender, message, timestamp) VALUES (?, ?, ?)",
                   (sender, message, timestamp))
    msg_id = cursor.lastrowid
    conn.commit()
    conn.close()
    emit('receive_message', {'id': msg_id, 'sender': sender, 'message': message, 'timestamp': timestamp}, broadcast=True)

@socketio.on('typing')
def handle_typing(data):
    emit('show_typing', {'sender': session.get('username')}, broadcast=True, include_self=False)

@socketio.on('connect')
def user_connected():
    username = session.get('username')
    if username:
        online_users.add(username)
        emit('online_status', list(online_users), broadcast=True)

@socketio.on('disconnect')
def user_disconnected():
    username = session.get('username')
    if username:
        online_users.discard(username)
        emit('online_status', list(online_users), broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
# app.py

# This file contains the main application logic for the chat application.   
