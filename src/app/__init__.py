import logging
import os
import requests

from flask import Flask, request, abort
from pymongo import MongoClient
from flask_restful import Api
from pymongo.errors import PyMongoError

from . import settings

from .resources import Home
from .resources import Video
from .exceptions import InvalidParamsException
from .exceptions import VideoNotFoundException

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


@app.errorhandler(InvalidParamsException)
def handle_bad_request(e):
    return {'errors': e.message}, 400


@app.errorhandler(PyMongoError)
def handle_db_errors(e):
    return {'errors': str(e)}, 500


@app.errorhandler(VideoNotFoundException)
def handle_video_not_found(e):
    return {'errors': e.message}, 404
