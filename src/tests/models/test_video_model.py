import unittest

from app.models.video import VideoModel
from mongoengine.errors import ValidationError


class TestVideoModel(unittest.TestCase):
    video_data = {
        'file_name': 'file_name_test',
        'file_size': '1024',
        'download_url': 'http//url.com',
        'datetime': None
    }
    video_error_body = {
        'file_name': 'file_name_test',
        'download_url': 'http//url.com',
        'datetime': '2020-05-19T12:00:01'
    }

    def test_to_default_datetime(self):
        video = VideoModel(**self.video_data)
        self.assertIsNotNone(video.datetime)

    def test_raise_validation_error_on_create(self):
        with self.assertRaises(ValidationError):
            VideoModel(**self.video_error_body)


if __name__ == '__main__':
    unittest.main()
