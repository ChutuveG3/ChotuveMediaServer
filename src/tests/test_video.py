import unittest
import mock

from app import app
from app.models.video import VideoModel
from mongoengine.errors import ValidationError

video_data = {
    'file_name': 'file_name_test',
    'file_size': '1024',
    'download_url': 'http//url.com'
}

video_success_body = {
    'file_name': 'file_name_test',
    'file_size': 1024,
    'download_url': 'http//url.com',
}

video_error_body = {
    'file_name': 'file_name_test',
    'download_url': 'http//url.com',
}


class TestVideoModel(unittest.TestCase):
    def test_to_default_datetime(self):
        video = VideoModel(**video_data)
        self.assertIsNotNone(video.datetime)

    def test_raise_validation_error_on_create(self):
        with self.assertRaises(ValidationError) as context:
            VideoModel(**video_error_body)


class TestVideoController(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    @mock.patch('app.repositories.video_repository.VideoRepository.save')
    def test_success_video_upload(self, mock_save):
        response = self.app.post('/videos', json=video_success_body)

        self.assertEqual(mock_save.call_count, 1)
        self.assertEqual(response.json, {})
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()