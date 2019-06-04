#!/usr/bin/env python3

from flask import Flask
app = Flask(__name__)

@app.route("/hello-world")
def hello():
    return "Hello world!"

if __name__ == "__main__":
    from gevent.pywsgi import WSGIServer
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()

    
