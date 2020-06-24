from flask_restful import Resource

from ..exceptions import InvalidParamsException
from ..repositories import *


class VideoById(Resource):

    def delete(self, video_id):
        try:
            video_id = int(video_id)
        except ValueError as e:
            raise InvalidParamsException(str(e))

        video = VideoRepository().find_by_id(id_list=[video_id])
        VideoRepository().delete(video[0])

        return {}, 200