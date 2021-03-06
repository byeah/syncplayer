from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

epoch = datetime.utcfromtimestamp(0)
delay = 2000    # milliseconds

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('my event', namespace='/test')
def test_message(message):
    params = {'name':'Server','data': message['data']}
    if message.get('initTime'):
        params['serverTime'] = int((datetime.utcnow() - epoch).total_seconds() * 1000)
    emit('my response', params)

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data'],'name':message['name']}, broadcast=True)

@socketio.on('video control', namespace='/test')
def test_message(message):
    params = {'actiontype': message['actiontype'], 'progress': message['progress']}
    if message['actiontype'] == 'play':
        params['ontime'] = int((datetime.utcnow() - epoch).total_seconds() * 1000) + delay
    emit('video control', params, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)
