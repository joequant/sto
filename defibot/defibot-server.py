#!/usr/bin/python3
from flask import Flask
from flask import Flask, request, jsonify
from ariadne import graphql_sync, make_executable_schema, gql, load_schema_from_path
from ariadne.constants import PLAYGROUND_HTML
from model import query

type_defs = gql(load_schema_from_path("./schema.graphql"))
schema = make_executable_schema(type_defs, query)

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

if __name__ == '__main__':
    app.run()
