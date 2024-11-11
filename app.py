from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize the shared counter
counter = 0

@app.route('/')
def index():
    return render_template('index.html')

# Handle button click event
@socketio.on('increment_counter')
def handle_increment():
    global counter
    counter += 1
    socketio.emit('update_counter', {'counter': counter})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)