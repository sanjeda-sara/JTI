from mitmproxy import http
import urllib.parse

# Define a variable to store the search query
search_query = ""

def extract_query(url):
    # Extract the query from the URL
    if "q=" in url:
        query = url.split("q=")[1].split("&")[0]
        return urllib.parse.unquote(query)
    return None

def calculate_result(query):
    try:
        result = eval(query)
        return result
    except (SyntaxError, NameError, TypeError):
        return None

def request(flow: http.HTTPFlow) -> None:
    global search_query
    url = flow.request.pretty_url
    if "www.google.com" in flow.request.host:
        query = extract_query(url)
        if query:
            search_query = query  # Store the search query

def response(flow: http.HTTPFlow) -> None:
    if "www.google.com" in flow.request.host:
        response_text = flow.response.text

        if "resultStats" in response_text:
            # Extract the search result from the response
            result_start = response_text.find("resultStats") + len("resultStats") + 2
            result_end = response_text.find("results")
            result = response_text[result_start:result_end].strip()
            print(f"Search Query: {search_query}")
            print(f"Search Result: {result}")

# Remove the previous `response` function and add the updated one.

