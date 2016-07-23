from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'name':'Server','data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data'],'name':message['name']}, broadcast=True)

@socketio.on('video control', namespace='/test')
def test_message(message):
    emit('video control', {'data': message['data'],'name':message['name']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
