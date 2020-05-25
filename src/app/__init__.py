import logging
import os

from flask import Flask
from pymongo import MongoClient
from flask_restful import Api
from pymongo.errors import PyMongoError

from . import settings

from .resources import Home
from .resources import Video
from .resources import VideosByUsername
from .exceptions import InvalidParamsException

app = Flask(__name__)
app.config["DEBUG"] = True
API = Api(app)

# Create and config. logger
LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT)
logger = logging.getLogger()

# Config. database and set default.
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/db'))
db = client.get_database(os.getenv('DB_NAME', 'test'))
logger.info(f'Connected to DB: {db.name}')

API.add_resource(Home, '/')
API.add_resource(Video, '/videos')
API.add_resource(VideosByUsername, '/videos/<username>')


@app.errorhandler(InvalidParamsException)
def handle_bad_request(e):
    return {'errors': e.message}, 400


@app.errorhandler(PyMongoError)
def handle_bad_request(e):
    return {'errors': str(e)}, 500
