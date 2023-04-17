from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'srecret!'
socketio = SocketIO(app)

users = []
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat_room', methods=['POST'])
def chat_room():
    username = request.form['username']
    if username in users:
        return redirect(url_for('index'))
    users.append(username)
    emit('user_joined', {'username':username}, broadcast=True)
    return render_template('chat_room.html', username=username, messages=messages)

@socketio.on('send_message')
def send_message(message):
    username = message['username']
    content = message['content']
    messages.append({'username': username, 'content': content})
    emit('new_message', {'username': username, 'content': content}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    username = request.sid
    users.remove(username)
    emit('user_left', {'username': username}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)