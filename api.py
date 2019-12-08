from flask import Flask, request, Response, abort
import huge
import json
from huge import FailedGenerationError

from flask import render_template

app = Flask(__name__)

huge.setup()

@app.route('/')
def root():
    return render_template('homegamebutnobodyturnedup.html')

@app.route("/api/querystring")
def querystring():
    try:
        output = huge.generate_from_query_string(request.args.get("query"))
        return json.dumps(output)
    except FailedGenerationError:
        return json.dumps("Failed to convert into a sick measurement..")
