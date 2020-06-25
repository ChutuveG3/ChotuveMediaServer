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

        app_delete_url = os.getenv('APP_BASE_URL', "") + f'/video/{video_id}'
        headers = {'content-type': 'application/json',
                   'authorization': request.headers.get('authorization')}
        response = requests.delete(app_delete_url, headers=headers)

        if response.status_code != 200:
            return {'error': 'app server error'}, 402

        repo.delete(video)
        return {}, 200
