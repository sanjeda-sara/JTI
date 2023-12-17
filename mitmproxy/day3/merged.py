import http.server
import socketserver
import threading
import time
from mitmproxy import http
from mitmproxy import master, options
from mitmproxy.addons import core
from mitmproxy.proxy import ProxyConfig, ProxyServer
from mitmproxy.tools.dump import DumpMaster

# Define a variable to store the captured data
captured_data = []

# Function to update the captured data in the background
def update_captured_data(flow):
    global captured_data
    if "jsonplaceholder.typicode.com" in flow.request.pretty_url:
        captured_data.append(flow.response.content)
        print(f"Captured data: {flow.response.content}")

# Start the MITMProxy
opts = options.Options(listen_host='0.0.0.0', listen_port=8080)
config = ProxyConfig(opts)
master = DumpMaster(opts)
master.server = ProxyServer(config)
master.addons.add(core.Core())
master.addons.add(http.HTTPMaster())

# Start the MITMProxy in a separate thread
mitm_thread = threading.Thread(target=master.run)
mitm_thread.daemon = True
mitm_thread.start()

# Define a custom request handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"""
                <html>
                    <body>
                        <h1>Captured Data</h1>
                        <ul>
                            {"".join([f"<li>{data}</li>" for data in captured_data])}
                        </ul>
                    </body>
                </html>
            """.encode('utf-8'))
        else:
            super().do_GET()

# Define the server address
host = 'localhost'
port = 4200

# Start the server with the custom request handler
with socketserver.TCPServer((host, port), MyHandler) as httpd:
    print(f'Serving on http://{host}:{port}')
    httpd.serve_forever()
