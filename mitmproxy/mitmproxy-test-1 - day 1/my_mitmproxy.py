
from mitmproxy import http
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


request()



