import logging
import os
from flask import Flask
from pymongo import MongoClient
from flask_restful import Api

from .resources import Home

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