import unittest

import mock
from app import app
from app.models.video import VideoModel
from mongoengine.errors import ValidationError
from app.exceptions.invalid_params_exception import InvalidParamsException

video_error_body = {
    'file_name': 'file_name_test',
    'download_url': 'http//url.com',
    'datetime': '2020-05-19T12:00:01'
}


class TestVideoModel(unittest.TestCase):
    video_data = {
        'file_name': 'file_name_test',
        'file_size': '1024',
        'download_url': 'http//url.com'
    }

    def test_to_default_datetime(self):
        video = VideoModel(**self.video_data)
        self.assertIsNotNone(video.datetime)

    def test_raise_validation_error_on_create(self):
        with self.assertRaises(ValidationError):
            VideoModel(**video_error_body)


class TestVideoController(unittest.TestCase):
    video_success_body = {
        'file_name': 'file_name_test',
        'file_size': 1024,
        'download_url': 'http//url.com',
        'datetime': '2020-05-19T12:00:01'
    }

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    @mock.patch('app.repositories.video_repository.VideoRepository.save')
    def test_success_video_upload(self, mock_save):
        response = self.app.post('/videos', json=self.video_success_body)

        self.assertEqual(mock_save.call_count, 1)
        self.assertEqual(response.json, {})
        self.assertEqual(response.status_code, 201)

    def test_validation_error_handle(self):
        response = self.app.post('/videos', json=video_error_body)

        self.assertDictEqual(response.json, {'errors': {'file_size': 'Field is required'}})
        self.assertEqual(response.status_code, 400)

    def test_date_validation_error(self):
        video_invalid_datetime = self.video_success_body.copy()
        video_invalid_datetime['datetime'] = 'invalid_datetime_format'
        response = self.app.post('/videos', json=video_invalid_datetime)

        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
