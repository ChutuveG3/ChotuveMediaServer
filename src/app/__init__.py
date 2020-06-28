import logging
import os

from flask import Flask, request
from pymongo import MongoClient
from flask_restful import Api
from pymongo.errors import PyMongoError

from . import settings

from .resources import Home
from .resources import Video
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
def auth():
    app_server_key = request.headers.get(['authorization'])
    admin_token = request.headers.get(['x_api_key'])

    # if admin_token:
    #     AuthService.validate_admin_token(admin_token)
    # elif app_server_key:
    #     AuthService.validate_app_server(app_server_key)
    # else:
    #     return {'errors': 'auth server error'}, 401
