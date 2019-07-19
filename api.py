from flask import Flask, request, Response, abort
import huge
import json

from flask import render_template

app = Flask(__name__)

huge.setup()

@app.route('/')
def root():
    return render_template('homegamebutnobodyturnedup.html')

@app.route('/api/bum')
def bum():
    try:
        value = request.args.get("value")
        value = float(value)
        unit = request.args.get("unit")
        output = huge.wide(unit, value)
        return json.dumps(output)
    except ValueError:
        abort(400)