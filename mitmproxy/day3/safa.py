from mitmproxy import http
import urllib.parse
import os

captured_data = []

def request(flow):
    url = flow.request.pretty_url
    if "q=" in url:  # Check if "q=" parameter exists in the URL
        query = url.split("q=")[1].split("&")[0]  # Extract the value of the "q" parameter
        query = urllib.parse.unquote(query)
        website = flow.request.pretty_host  # Extract the website
        print(f"Website: {website}")
        print(f"Search Query: {query}")
    print("----------------")
    print(flow.request.text)

def response(flow: http.HTTPFlow):
    if "jsonplaceholder.typicode.com" in flow.request.pretty_url:
        captured_data.append(flow.response.text)

if __name__ == '__main__':
    # Specify the network interface for capturing traffic (e.g., a VPN interface)
    interface = "tun0"  # Replace with the name of your VPN interface

    # Set up the environment variable to ensure mitmproxy captures traffic on the specified interface
    os.environ['MITMPROXY_MODE'] = 'transparent'
    os.environ['MITMPROXY_INTERFACE'] = interface

    from mitmproxy.tools.main import mitmdump
    mitmdump(['-s', __file__])

# After capturing the data, you can choose to save it or process it as needed
