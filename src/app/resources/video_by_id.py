import marshmallow
from flask_restful import Resource
from ..exceptions import InvalidParamsError
from ..repositories import VideoRepository
from ..schemas import DeleteVideoByIdSchema, GetVideosSchema
from ..services.decorators import admin_authenticate


class VideoById(Resource):
    method_decorators = {'delete': [admin_authenticate]}

    def delete(self, video_id):
        try:
            DeleteVideoByIdSchema().load({GetVideosSchema.ID_KEY: video_id})
        except marshmallow.ValidationError:
            raise InvalidParamsError()

        repo = VideoRepository()
        video = repo.find_by_id(id_list=[video_id]).pop()
        repo.delete(video)

        return {}, 200
