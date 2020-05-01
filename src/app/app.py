import os
from flask import Flask, escape, request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods = ['GET'])

def home():
	return {'example': 'hello world'}

if __name__ == '__main__':
    app.run()
