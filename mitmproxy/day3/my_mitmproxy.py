from mitmproxy import http
import urllib.parse
from stream import realtime_value

captured_data = []

def request(flow):
    url = flow.request.pretty_url
    if "q=" in url:  # Check if "q=" parameter exists in the URL
        query = url.split("q=")[1].split("&")[0]  # Extract the value of the "q" parameter
        query = urllib.parse.unquote(query)
        website = flow.request.pretty_host  # Extract the website
        print(f"Website: {website}")
        print(f"Search Query: {query}")
    print(">>>>>>>>>>>>>>>>>>>>>>>>")
    print(url)
    print("-----------------------------------------------------")
    print(flow.request.json())
    realtime_value = flow.request.json()
    print("===========================================")
    print(flow.response.content)

def response(flow: http.HTTPFlow):
    
    # if "jsonplaceholder.typicode.com" in flow.request.pretty_url:
    #     captured_data.append(flow.response.text)
    pass

if __name__ == '__main__':
    from mitmproxy.tools.main import mitmdump
    mitmdump(['-q', '-s', __file__])


