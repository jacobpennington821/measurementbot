from flask import Flask, request
import huge

app = Flask(__name__)

@app.route('/bum')
def bum():
    value = request.args.get("value")
    unit = request.args.get("unit")
    output = huge.wide(value, unit)
    return 'WIDE'