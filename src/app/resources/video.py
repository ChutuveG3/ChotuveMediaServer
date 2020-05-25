from datetime import datetime
from flask_restful import Resource
from flask import request
from mongoengine import ValidationError

from ..models import VideoModel
from ..repositories import *
from ..exceptions import InvalidParamsException


class Video(Resource):
    ID_KEY = 'id'
    SIZE_KEY = 'file_size'
    NAME_KEY = 'file_name'
    DOWNLOAD_URL_KEY = 'download_url'
    DATETIME_KEY = 'datetime'
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    LIMIT_PARAM = 'limit'
    LIMIT_DEFAULT = 0
    OFFSET_PARAM = 'offset'
    OFFSET_DEFAULT = 0

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
            raise InvalidParamsException(str(e))
        except ValidationError as e:
            raise InvalidParamsException(e.to_dict())

        return {self.ID_KEY: video._id}, 201

    def get(self):
        try:
            limit = int(request.args.get(self.LIMIT_PARAM, self.LIMIT_DEFAULT))
            offset = int(request.args.get(self.OFFSET_PARAM, self.OFFSET_DEFAULT))
        except ValueError as e:
            raise InvalidParamsException(str(e))
        result = VideoRepository().find_all(limit, offset)
        videos = [self.map_video(video) for video in result]

        return videos, 200, {'total': len(videos)}

    def map_video(self, video):
        return {self.ID_KEY: video._id,
                self.SIZE_KEY: video.file_size,
                self.DOWNLOAD_URL_KEY: video.download_url,
                self.DATETIME_KEY: video.datetime.strftime(self.DATE_FORMAT)}
