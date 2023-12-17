
#=============================================================================================================#    
                       #ORIGINAL
#=============================================================================================================# 

# from mitmproxy import http

# def request(flow: http.HTTPFlow) -> None:
#     # Print incoming requests
#     print(f"Incoming Request: {flow.request.pretty_url}")

# def response(flow: http.HTTPFlow) -> None:
#     # Print outgoing responses
#     print(f"Outgoing Response: {flow.request.pretty_url}")



# Run the mitmproxy with this script
# mitmproxy -s my_mitmproxy.py

#=============================================================================================================#    
                       #END OF ORIGINAL
#=============================================================================================================# 

# from mitmproxy import http

# def request(flow: http.HTTPFlow) -> None:
#     # Extract and print the search Query from the URL
#     url = flow.request.pretty_url
#     if "q=" in url:  # Check if "q=" parameter exists in the URL
#         query = url.split("q=")[1].split("&")[0]  # Extract the value of the "q" parameter
#         print(f"Search Query: {query}")

# def response(flow: http.HTTPFlow) -> None:
#     # Extract and print the name of the website being accessed
#     url = flow.request.pretty_url
#     if "://" in url:
#         domain = url.split("://")[1].split("/")[0]  # Extract the domain from the URL
#         print(f"Website: {domain}")

##==================================================================================================##
##==================================================================================================##
# from mitmproxy import http

# def request(flow: http.HTTPFlow) -> None:
#     # Extract and print the search Query from the URL
#     url = flow.request.pretty_url
#     if "q=" in url:  # Check if "q=" parameter exists in the URL
#         query = url.split("q=")[1].split("&")[0]  # Extract the value of the "q" parameter
#         website = flow.request.pretty_host  # Extract the website

#         # Print the website and the search query
#         print(f"Website: {website}")
#         print(f"Search Query: {query}")

# def response(flow: http.HTTPFlow) -> None:
#     pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




#=============================================================================================================#    
                        #MODIFIED CODE from JSON to idek
#=============================================================================================================# 
# from mitmproxy import http

# # Create a dictionary to store search queries for each website
# queries_by_website = {}

# def request(flow: http.HTTPFlow) -> None:
#     # Extract the search query from the URL
#     query_params = flow.request.query
#     if 'q' in query_params:
#         search_query = query_params['q']
#     else:
#         search_query = "No search query found"

#     # Extract the website name
#     website = flow.request.pretty_host

#     # Store the search query for the website
#     if website not in queries_by_website:
#         queries_by_website[website] = []
#     queries_by_website[website].append(search_query)

# def response(flow: http.HTTPFlow) -> None:
#     # Do something with the response if needed
#     pass

# from mitmproxy.tools.main import mitmdump

# # mitmdump is a built-in command that starts mitmproxy
# # Use -s <your_script.py> to run your script
# mitmdump(['-s', __file__])

# # Print the collected data in the desired format
# for website, queries in queries_by_website.items():
#     print(f"Website: {website}")
#     for query in queries:
#         print(f"  Search Query: {query}")




#=============================================================================================================#    
 #                       MODIFIED CODE from JSON to the default output format of Mitmproxy
#=============================================================================================================# 
# from mitmproxy import http

# def request(flow: http.HTTPFlow) -> None:
#     # Extract and print the search Query from the URL
#     url = flow.request.pretty_url
#     if "q=" in url:  # Check if "q=" parameter exists in the URL
#         query = url.split("q=")[1].split("&")[0]  # Extract the value of the "q" parameter
#         print(f"Search Query: {query}")

# def response(flow: http.HTTPFlow) -> None:
#     # Extract and print the name of the website being accessed
#     url = flow.request.pretty_url
#     if "://" in url:
#         domain = url.split("://")[1].split("/")[0]  # Extract the domain from the URL
#         print(f"Website: {domain}")

# from mitmproxy.tools.main import mitmdump

# mitmdump is a built-in command that starts mitmproxy
# Use -s <your_script.py> to run your modified script
#mitmdump(['-s', __file__])

#===================================================================================================================#
# from mitmproxy.tools.main import mitmdump
# # mitmdump is a built-in command that starts mitmproxy
# # Use -s <your_script.py> to run your script
# mitmdump(['-s', __file__])

# from mitmproxy import http

# def request(flow: http.HTTPFlow) -> None:
#     # Print incoming requests
#     print(f"Incoming Request: {flow.request.pretty_url}")

# def response(flow: http.HTTPFlow) -> None:
#     # Print outgoing responses
#     print(f"Outgoing Response: {flow.request.pretty_url}")

# from mitmproxy.tools.main import mitmdump

# if __name__ == '__main__':
#     # Use the script file's name as a string
#     script_file = __file__
#     # Start mitmdump and pass the script file's name as an argument
#     mitmdump(['-s', script_file])