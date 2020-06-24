from flask_restful import Resource
from ..repositories import *


class VideoById(Resource):

    def delete(self, video_id):
        video = VideoRepository().find_by_id(id_list=[int(video_id)])
        VideoRepository().delete(video[0])

        return {}, 200