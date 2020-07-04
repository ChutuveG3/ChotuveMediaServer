import marshmallow
from flask_restful import Resource
from flask import request
from mongoengine import ValidationError
from marshmallow import ValidationError

from ..models import VideoModel
from ..repositories import *
from ..exceptions import InvalidParamsError
from ..schemas import CreateVideoSchema
from ..services.decorators import server_or_admin_authenticate


class Video(Resource):
    method_decorators = {'get': [server_or_admin_authenticate],
                         'post': [server_or_admin_authenticate]}
    ID_KEY = 'id'
    LIMIT_PARAM = 'limit'
    LIMIT_DEFAULT = 0
    PAGE_PARAM = 'page'
    PAGE_DEFAULT = 0

    def post(self):
        try:
            parse_body = request.get_json(force=True)
            video_schema = CreateVideoSchema()
            video_data = video_schema.load(parse_body)

            video = VideoModel(file_size=video_data.get(video_schema.SIZE_KEY),
                               file_name=video_data.get(video_schema.NAME_KEY),
                               download_url=video_data.get(video_schema.DOWNLOAD_URL_KEY),
                               datetime=video_data.get(video_schema.UPLOAD_DATE_KEY)
                               )

            VideoRepository().save(video)
        except (ValueError, TypeError) as e:
            raise InvalidParamsError(str(e))
        except (ValidationError, marshmallow.ValidationError) as e:
            raise InvalidParamsError()

        return {self.ID_KEY: video._id}, 201

    def get(self):
        try:
            id_list = [int(x) for x in request.args.getlist(self.ID_KEY)]
            limit = int(request.args.get(self.LIMIT_PARAM, self.LIMIT_DEFAULT))
            page = int(request.args.get(self.PAGE_PARAM, self.PAGE_DEFAULT))
        except ValueError as e:
            raise InvalidParamsError(str(e))

        result = VideoRepository().find_by_id(id_list, limit, page)
        videos = [self.map_video(video) for video in result]

        return videos, 200, {'total': len(videos)}

    def map_video(self, video):
        return {
            self.ID_KEY: video._id,
            CreateVideoSchema.NAME_KEY: video.file_name,
            CreateVideoSchema.DOWNLOAD_URL_KEY: video.download_url,
            CreateVideoSchema.UPLOAD_DATE_KEY: video.datetime.strftime(CreateVideoSchema.DATE_FORMAT),
            CreateVideoSchema.SIZE_KEY: video.file_size
        }
