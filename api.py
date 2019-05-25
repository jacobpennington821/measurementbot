from flask import Flask, request
import .wide from huge

app = Flask(__name__)

@app.route('/bum')
def bum():
    return 'something'