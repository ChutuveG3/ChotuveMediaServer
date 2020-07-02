from flask_restful import Resource
from ..exceptions import InvalidParamsError
from ..repositories import VideoRepository
from ..services.decorators import app_server_authenticate


class VideoById(Resource):
    method_decorators = {'delete': [app_server_authenticate]}

    def delete(self, video_id):
        try:
            video_id = int(video_id)
        except ValueError as e:
            raise InvalidParamsError(str(e))

        repo = VideoRepository()
        video = repo.find_by_id(id_list=[video_id]).pop()
        repo.delete(video)

        return {}, 200
