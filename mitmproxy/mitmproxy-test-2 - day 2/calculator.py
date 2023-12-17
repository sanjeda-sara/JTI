import requests
from bs4 import BeautifulSoup

def get_google_search_result(query):
    # Create a Google search URL
    search_url = f"https://www.google.com/search?q={query}"

    # Send an HTTP GET request
    response = requests.get(search_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the search result (usually the first one)
        search_result = soup.find('div', class_='BNeawe iBp4i AP7Wnd').get_text()

        return search_result

    return None

if __name__ == "__main__":
    query = input("Enter your search query: ")
    result = get_google_search_result(query)

    if result:
        print(f"Search Query: {query}")
        print(f"Search Result: {result}")
    else:
        print("Failed to fetch search result.")
