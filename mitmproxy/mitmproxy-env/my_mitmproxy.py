import http.server
import socketserver
import threading
import time
from mitmproxy import http
import urllib.parse

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
port = 8080

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
    
    # Function to intercept network traffic using mitmproxy
    def intercept_network_traffic():
        #from mitmproxy import http
        import urllib.parse

        def request(flow: http.HTTPFlow) -> None:
            # Extract and print the search Query from the URL
            url = flow.request.pretty_url
            if "q=" in url:  # Check if "q=" parameter exists in the URL
                query = url.split("q=")[1].split("&")[0]  # Extract the value of the "q" parameter

                # Replace '+' with space in the query
                query = urllib.parse.unquote(query)

                website = flow.request.pretty_host  # Extract the website

                # Print the website and the search query
                print(f"Website: {website}")
                print(f"Search Query: {query}")

        def response(flow: http.HTTPFlow) -> None:
            pass

        # Configure mitmproxy and run
        from mitmproxy.tools.main import mitmdump
        #mitmdump(['-s', __file__])

    # Start the mitmproxy functionality in a separate thread
    mitm_thread = threading.Thread(target=intercept_network_traffic)
    mitm_thread.start()

    # Serve the web page and update the value
    httpd.serve_forever()
