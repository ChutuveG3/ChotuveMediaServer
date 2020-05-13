from flask_restful import Resource
from flask import request, Response

from ..models import VideoModel
from ..repositories import *


class Video(Resource):
    def post(self):
        parse_body = request.get_json(force=True)
        video = VideoModel(**parse_body)
        VideoRepository().save(video)

        return Response("{}", status=201, mimetype='application/json')




