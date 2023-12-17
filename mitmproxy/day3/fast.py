"""
Host a WSGI app in mitmproxy.

This example shows how to graft a WSGI app onto mitmproxy. In this
instance, we're using the Flask framework (http://flask.pocoo.org/) to expose
a single simplest-possible page.
"""
from flask import Flask

from mitmproxy.addons import asgiapp

app = Flask("proxapp")


@app.route("/")
def hello_world() -> str:
    return "Hello World!"


addons = [
    # Host app at the magic domain "example.com" on port 80. Requests to this
    # domain and port combination will now be routed to the WSGI app instance.
    asgiapp.WSGIApp(app, "example.com", 80),
    # TLS works too, but the magic domain needs to be resolvable from the mitmproxy machine due to mitmproxy's design.
    # mitmproxy will connect to said domain and use its certificate but won't send any data.
    # By using `--set upstream_cert=false` and `--set connection_strategy_lazy` the local certificate is used instead.
    # asgiapp.WSGIApp(app, "example.com", 443),
]