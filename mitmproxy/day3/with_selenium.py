from mitmproxy import http
import threading
import queue
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.parse

# Initialize a queue to communicate between threads
user_input_queue = queue.Queue()

# Initialize a Selenium WebDriver (you may need to specify the driver executable path)
driver = webdriver.Chrome()
website_actions = {}

# Thread to capture user input
def capture_user_input():
    while True:
        user_input = input("Enter your input: ")
        if user_input.lower() == "exit":
            user_input_queue.put(None)  # Signal the main thread to exit
        else:
            user_input_queue.put(user_input)

# Thread to interact with Google Calculator
def interact_with_google_calculator():
    while True:
        user_input = user_input_queue.get()
        if user_input:
            driver.get("https://www.google.com")
            search_box = driver.find_element_by_name("q")
            search_box.clear()
            search_box.send_keys(user_input)
            search_box.send_keys(Keys.RETURN)

# Start the user input capture thread
user_input_thread = threading.Thread(target=capture_user_input)
user_input_thread.daemon = True
user_input_thread.start()

# Start the interaction thread with Google Calculator
interaction_thread = threading.Thread(target=interact_with_google_calculator)
interaction_thread.daemon = True
interaction_thread.start()

def request(flow: http.HTTPFlow):
    url = flow.request.pretty_url
    if "q=" in url:
        query = url.split("q=")[1].split("&")[0]
        website = flow.request.pretty_host
        print(f"Website: {website}")
        print(f"Search Query: {query}")

        user_input = user_input_queue.get()
        if user_input:
            website_actions[website] = []  # Initialize actions list for the website
            print(f"User Input: {user_input}")
            website_actions[website].append(f"Performed a search for: {query}")

def response(flow: http.HTTPFlow):
    pass  # No action needed in response

if __name__ == '__main__':
    from mitmproxy.tools.main import mitmdump
    mitmdump(['-q', '-s', __file__])
