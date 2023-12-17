# mitmproxy_scripts.py
from mitmproxy import http
from flask import Flask, render_template
from flask_socketio import SocketIO
import json  # Import the json module

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

captured_data = []

def request(flow: http.HTTPFlow):
    if "jsonplaceholder.typicode.com" in flow.request.pretty_url:
        data = {
            "url": flow.request.url,
            "method": flow.request.method,
            "headers": dict(flow.request.headers),
            "body": flow.request.text,
        }
        captured_data.append(data)
        # Emit data as a string (convert to JSON first)
        socketio.emit('new_data', json.dumps(data))

@app.route('/')
def index1():
    return render_template('index1.html')

@socketio.on('connect')
def handle_connect():
    for data in captured_data:
        socketio.emit('new_data', json.dumps(data))

if __name__ == '__main__':
    from mitmproxy.tools.main import mitmdump
    mitmdump(['-s', __file__])
    socketio.run(app)
