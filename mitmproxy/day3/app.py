from flask import Flask, render_template
from flask_socketio import SocketIO
import json
from mitproxy_script import captured_data

# SocketIO.init_app(app, async_mode='threading')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
SocketIO = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@SocketIO.on('connect')
def handle_connect():
    for data in captured_data:
        SocketIO.emit('new_data', json.dumps(data))
        print("------------------->")
        print(data)

if __name__ == '__main__':
    SocketIO.run(app)
