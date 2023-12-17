import http.server
import socketserver

# Import the threading module to run the server and update values concurrently
import threading
import time

# Define a variable that can be updated in real-time
realtime_value = "Initial Value"

# Create a custom request handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global realtime_value  # Access the global variable

        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"""
                <html>
                    <body>
                        <h1>Real-Time Value: <span id="realtime">{realtime_value}</span></h1>
                        <script>
                            // JavaScript to update the value every 2 seconds
                            function updateRealtimeValue() {{
                                setInterval(function() {{
                                    fetch('/get_realtime_value')
                                        .then(response => response.text())
                                        .then(data => document.getElementById('realtime').textContent = data);
                                }}, 2000); // Update every 2 seconds
                            }}
                            updateRealtimeValue();
                        </script>
                    </body>
                </html>
            """.encode('utf-8'))
        elif self.path == '/get_realtime_value':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(realtime_value.encode('utf-8'))
        else:
            super().do_GET()

# Define the server address
host = 'localhost'
port = 8100

# Function to update the realtime value in the background
def update_realtime_value():
    global realtime_value
    while True:
        # Simulate real-time updates here (replace with your own logic)
        new_value = str(time.time())
        realtime_value = new_value
        time.sleep(2)  # Update every 2 seconds

# Start the value update thread
update_thread = threading.Thread(target=update_realtime_value)
update_thread.daemon = True
update_thread.start()

# Start the server with the custom request handler
with socketserver.TCPServer((host, port), MyHandler) as httpd:
    print(f'Serving on http://{host}:{port}')
    httpd.serve_forever()