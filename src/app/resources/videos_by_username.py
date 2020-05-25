from flask_restful import Resource
from flask import request

from . import Video
from ..repositories import *
from ..exceptions import InvalidParamsException


class VideosByUsername(Resource):
    def get(self, username):
        try:
            limit = int(request.args.get(Video.LIMIT_PARAM, Video.LIMIT_DEFAULT))
            offset = int(request.args.get(Video.OFFSET_PARAM, Video.OFFSET_DEFAULT))
        except ValueError as e:
            raise InvalidParamsException(str(e))
        result = VideoRepository().find_by_username(username, limit, offset)
        videos = [Video().map_video(video) for video in result]

        return videos, 200, {'total': len(videos)}
