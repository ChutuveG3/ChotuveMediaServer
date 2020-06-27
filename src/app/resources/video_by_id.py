import requests
import os

from flask_restful import Resource
from ..exceptions import InvalidParamsException
from ..repositories import *
from flask import request


class VideoById(Resource):
    def delete(self, video_id):
        try:
            video_id = int(video_id)
        except ValueError as e:
            raise InvalidParamsException(str(e))

        repo = VideoRepository()
        video = repo.find_by_id(id_list=[video_id]).pop()
        repo.delete(video)

        return {}, 200
