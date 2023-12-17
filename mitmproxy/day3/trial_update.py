from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from mitmproxy import http
import urllib.parse

# Initialize a Selenium WebDriver (you may need to specify the driver executable path)
driver = webdriver.Chrome()

# Define a dictionary to store website actions
website_actions = {}

def request(flow: http.HTTPFlow):
    url = flow.request.pretty_url
    if "q=" in url:  # Check if "q=" parameter exists in the URL
        query = url.split("q=")[1].split("&")[0]  # Extract the value of the "q" parameter
        query = urllib.parse.unquote(query)
        website = flow.request.pretty_host  # Extract the website
        if website not in website_actions:
            website_actions[website] = []  # Initialize actions list for the website
        print(f"Website: {website}")
        print(f"Search Query: {query}")
        website_actions[website].append(f"Performed a search for: {query}")

def response(flow: http.HTTPFlow):
    pass  # No action needed in response

def interact_with_google_calculator(query):
    driver.get("https://www.google.com")
    search_box = driver.find_element_by_name("q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

if __name__ == '__main__':
    from mitmproxy.tools.main import mitmdump
    mitmdump(['-q', '-s', __file__])

    while True:
        user_input = input("Enter your input: ")
        if user_input.lower() == "exit":
            break
        interact_with_google_calculator(user_input)
