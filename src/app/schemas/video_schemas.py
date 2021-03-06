from marshmallow import fields, Schema


class CreateVideoSchema(Schema):
    SIZE_KEY = 'file_size'
    NAME_KEY = 'file_name'
    DOWNLOAD_URL_KEY = 'download_url'
    UPLOAD_DATE_KEY = 'datetime'
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    file_name = fields.String(attribute=NAME_KEY, required=True)
    file_size = fields.Integer(attribute=SIZE_KEY, required=True)
    datetime = fields.NaiveDateTime(DATE_FORMAT, attribute=UPLOAD_DATE_KEY, allow_none=True)
    download_url = fields.String(required=True)


class GetVideosSchema(Schema):
    ID_KEY = 'id'
    LIMIT_KEY = 'limit'
    LIMIT_DEFAULT = 0
    PAGE_KEY = 'page'
    PAGE_DEFAULT = 0

    id = fields.List(fields.Integer, attribute=ID_KEY, allow_none=True)
    page = fields.Integer(attribute=PAGE_KEY, allow_none=True)
    limit = fields.Integer(attribute=LIMIT_KEY, allow_none=True)


class DeleteVideoByIdSchema(Schema):
    id = fields.Integer(required=True)

