import json

from flask import Flask, request, Response, render_template
import generator
from generator import FailedGenerationError

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
        return Response("Failed to convert into a sick measurement..", 400)
