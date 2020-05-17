from flask_restful import Resource
from src.app.version import Version


class Home(Resource):
    def get(self):
        return {'version': f'{Version.get()}'}

