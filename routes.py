from flask import Flask, request, Response, abort
import generator
import json
from generator import FailedGenerationError

from flask import render_template

app = Flask(__name__)

generator.setup()

@app.route('/')
def root():
    return render_template('home.html')

@app.route("/api/querystring")
def querystring():
    try:
        output = generator.generate_from_query_string(request.args.get("query"))
        return json.dumps(output)
    except FailedGenerationError:
        return json.dumps("Failed to convert into a sick measurement..")
