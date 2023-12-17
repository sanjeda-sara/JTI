from mitmproxy import http
import json
from flask_socketio import SocketIO

captured_data = []

def request(flow: http.HTTPFlow):
    if flow:
        # data = {
        #     "url": flow.request.url,
        #     "method": flow.request.method,
        #     "headers": dict(flow.request.headers),
        #     "body": flow.request.text,
        # }
        # captured_data.append(data)
        temp = socketio.emit('new_data', json.dumps(flow.request.json()))

        print(">>>>>>>----------------------------------------------------------------->")
        print(temp)

def response(flow: http.HTTPFlow):
    # if "jsonplaceholder.typicode.com" in flow.request.pretty_url:
    #     data = {
    #         "status_code": flow.response.status_code,
    #         "headers": dict(flow.response.headers),
    #         "body": flow.response.text,
    #     }
    #     captured_data.append(data)
    #     socketio.emit('new_data', json.dumps(data))
    pass

if __name__ == '__main__':
    from mitmproxy.tools.main import mitmdump
    mitmdump(['-s', __file__])