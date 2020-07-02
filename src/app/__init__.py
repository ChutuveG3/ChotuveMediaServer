import logging
import os

from flask import Flask, request
from pymongo import MongoClient
from flask_restful import Api
from pymongo.errors import PyMongoError

from . import settings

from .resources import Home
from .resources import Video
from .resources.video_by_id import VideoById
from .services import AuthService
from .exceptions import *


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
API.add_resource(VideoById, '/videos/<video_id>')


@app.errorhandler(InvalidParamsError)
def handle_bad_request(e):
    return {'errors': e.message}, 400


@app.errorhandler(PyMongoError)
def handle_db_errors(e):
    return {'errors': str(e)}, 500


@app.errorhandler(VideoNotFoundError)
def handle_video_not_found(e):
    return {'errors': e.message}, 404


@app.errorhandler(AuthServerError)
def handle_auth_server_error(e):
    return {'errors': 'auth server error'}, 502


@app.before_request
def auth_before_request():
    # TODO: refactor this
    if request.endpoint == 'home':
        return

    admin_token = request.headers.get('authorization')
    app_server_key = request.headers.get('x_api_key')
    if not AuthService.validate_admin_token(admin_token) and \
            not AuthService.validate_app_server(app_server_key):
        return {'errors': 'authorization error'}, 401


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
