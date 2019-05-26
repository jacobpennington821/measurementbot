from flask import Flask, request
import huge
import json

from flask import render_template

app = Flask(__name__)

huge.setup()

@app.route('/')
def root(name=None):
    return render_template('homegamebutnobodyturnedup.html', name=name)

@app.route('/api/bum')
def bum():
    value = request.args.get("value")
    unit = request.args.get("unit")
    output = huge.wide(unit, value)
    return json.dumps(output)
