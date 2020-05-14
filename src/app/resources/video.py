from datetime import datetime
from flask_restful import Resource
from flask import request, Response

from ..models import VideoModel
from ..repositories import *


class Video(Resource):
    def post(self):
        parse_body = request.get_json(force=True)
        if parse_body.get('datetime'):
            parse_body['datetime'] = datetime.strptime(parse_body['datetime'],
                                                       "%Y-%m-%dT%H:%M:%S")

        video = VideoModel(**parse_body)
        VideoRepository().save(video)

        return Response("{}", status=201, mimetype='application/json')




