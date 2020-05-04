import os
import logging
from flask import Flask, escape, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
app.config["DEBUG"] = True

# Create and config. logger
LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT)
logger = logging.getLogger()

# Config. database and set default.
client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017/db'))
db = client.get_database(os.getenv('DB_NAME', 'test'))
logger.info(f'Connected to DB: {db.name}')


@app.route('/', methods=['GET'])
def home():
    logger.info('Hello world')
    return {'example': 'hello world'}


if __name__ == '__main__':
    app.run()
