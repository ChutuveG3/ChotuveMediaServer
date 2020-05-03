import os
import logging
from flask import Flask, escape, request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

# Create and config. logger
LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT)
logger = logging.getLogger()


@app.route('/', methods=['GET'])
def home():
    logger.info('Hello world')
    return {'example': 'hello world'}


if __name__ == '__main__':
    app.run()
