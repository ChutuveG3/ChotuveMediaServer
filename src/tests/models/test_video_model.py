import unittest
from datetime import datetime

from app.models.video import VideoModel
from mongoengine.errors import ValidationError

from app.schemas import CreateVideoSchema


class TestVideoModel(unittest.TestCase):
    video_data = {
        CreateVideoSchema.NAME_KEY: 'file_name_test',
        CreateVideoSchema.SIZE_KEY: 1024,
        CreateVideoSchema.DOWNLOAD_URL_KEY: 'https://url.com',
        CreateVideoSchema.UPLOAD_DATE_KEY: datetime.strptime('2020-05-19T12:00:01',
                                                             CreateVideoSchema.DATE_FORMAT)
    }

    def test_create_video_success(self):
        video = VideoModel(**self.video_data)

        self.assertEqual(video.file_name, self.video_data.get('file_name'))

    def test_create_video_without_datetime_should_not_none(self):
        copy = self.video_data.copy()
        copy[CreateVideoSchema.UPLOAD_DATE_KEY] = None

        video = VideoModel(**copy)
        self.assertIsNotNone(video.datetime)

    def test_data_without_file_name_should_raise_validation_error(self):
        invalid_data = self.video_data.copy()
        invalid_data.pop(CreateVideoSchema.NAME_KEY)

        with self.assertRaises(ValidationError):
            VideoModel(**invalid_data)

    def test_invalid_url_should_raise_validation_error(self):
        invalid_url = self.video_data.copy()
        invalid_url[CreateVideoSchema.DOWNLOAD_URL_KEY] = 'https://not_url'

        with self.assertRaises(ValidationError):
            VideoModel(**invalid_url)

    def test_negative_file_size_should_raise_validation_error(self):
        invalid_file_size = self.video_data.copy()
        invalid_file_size[CreateVideoSchema.SIZE_KEY] = -10

        with self.assertRaises(ValidationError):
            VideoModel(**invalid_file_size)

    def test_max_file_name_lenght_should_raise_validation_error(self):
        invalid_file_name = self.video_data.copy()
        invalid_file_name[CreateVideoSchema.NAME_KEY] = 'Hello' * 100

        with self.assertRaises(ValidationError):
            VideoModel(**invalid_file_name)


if __name__ == '__main__':
    unittest.main()
