from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import re
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '13344'
socketio = SocketIO(app)

# Store messages and users
messages = []
users = set()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/join', methods=['POST'])
def join():
    email = request.form.get('email')
    pin = request.form.get('pin')
    
    # Validate email domain and pin
    if not email.endswith('@iitj.ac.in') or pin != '1234':
        return "Invalid email or PIN", 400
    
    session['email'] = email
    users.add(email)
    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', messages=messages, email=session['email'])

@socketio.on('message')
def handle_message(data):
    if 'email' in session:
        message = {
            'user': session['email'],
            'text': data['message'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        messages.append(message)
        emit('message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True) 