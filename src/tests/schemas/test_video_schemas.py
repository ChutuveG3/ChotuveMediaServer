import unittest

from app.schemas import CreateVideoSchema
from marshmallow import ValidationError

from src.app.schemas.video_schemas import GetVideosSchema


class TestVideoModel(unittest.TestCase):
    create_video_data = {
        CreateVideoSchema.NAME_KEY: 'file_name_test',
        CreateVideoSchema.SIZE_KEY: 1024,
        CreateVideoSchema.DOWNLOAD_URL_KEY: 'https://url.com',
        CreateVideoSchema.UPLOAD_DATE_KEY: '2020-05-19T22:00:01'
    }

    def test_create_video_schema_success(self):
        video_schema = CreateVideoSchema()
        video_data = video_schema.load(self.create_video_data)
        date = video_data.get(video_schema.UPLOAD_DATE_KEY).strftime(video_schema.DATE_FORMAT)

        self.assertEqual(video_data.get(video_schema.NAME_KEY), 'file_name_test')
        self.assertEqual(video_data.get(video_schema.SIZE_KEY), 1024)
        self.assertEqual(video_data.get(video_schema.DOWNLOAD_URL_KEY), 'https://url.com')
        self.assertEqual(date, '2020-05-19T22:00:01')

    def test_create_video_schema_fail_should_raise_validation_error(self):
        video_schema = CreateVideoSchema()
        copy_data = self.create_video_data.copy()
        copy_data.pop(video_schema.NAME_KEY)

        with self.assertRaises(ValidationError):
            video_schema.load(copy_data)

    def test_create_video_schema_not_required_upload_date(self):
        video_schema = CreateVideoSchema()
        copy_data = self.create_video_data.copy()
        copy_data.pop(video_schema.UPLOAD_DATE_KEY)
        video_data = video_schema.load(copy_data)

        self.assertIsNone(video_data.get(video_schema.UPLOAD_DATE_KEY))

    def test_get_video_schema_success(self):
        query_params = {
            "page": 10,
            "limit": 10,
            "id": [1, 4, 6, 7, 8]
        }
        schema = GetVideosSchema()
        video_data = schema.load(query_params)

        self.assertEqual(video_data.get(schema.PAGE_KEY), 10)
        self.assertEqual(video_data.get(schema.LIMIT_KEY), 10)
        self.assertEqual(video_data.get(schema.ID_KEY), [1, 4, 6, 7, 8])


if __name__ == '__main__':
    unittest.main()
