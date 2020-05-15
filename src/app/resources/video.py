from datetime import datetime
from flask_restful import Resource
from flask import request, Response
from mongoengine import ValidationError

from ..models import VideoModel
from ..repositories import *


class Video(Resource):
    SIZE_KEY = 'file_size'
    NAME_KEY = 'file_name'
    DOWNLOAD_URL_KEY = 'download_url'
    DATETIME_KEY = 'datetime'
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def post(self):
        try:
            parse_body = request.get_json(force=True)
            video = VideoModel(file_size=parse_body.get(self.SIZE_KEY),
                               file_name=parse_body.get(self.NAME_KEY),
                               download_url=parse_body.get(self.DOWNLOAD_URL_KEY),
                               datetime=datetime.strptime(parse_body.get(self.DATETIME_KEY),
                                                          self.DATE_FORMAT)
                               )
            VideoRepository().save(video)
        except (ValueError, TypeError) as e:
            raise ValidationError

        return Response("{}", status=201, mimetype='application/json')
