import unittest

import mock
from app import app
from pymongo.errors import DuplicateKeyError


class TestVideoController(unittest.TestCase):
    video_success_body = {
        'file_name': 'file_name_test',
        'file_size': 1024,
        'download_url': 'http//url.com',
        'datetime': '2020-05-19T12:00:01'
    }
    video_error_body = {
        'file_name': 'file_name_test',
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
        self.assertTrue('id' in response.json)
        self.assertEqual(response.status_code, 201)

    def test_validation_error_handle(self):
        response = self.app.post('/videos', json=self.video_error_body)

        self.assertDictEqual(response.json, {'errors': {'file_size': 'Field is required'}})
        self.assertEqual(response.status_code, 400)

    def test_date_validation_error(self):
        video_invalid_datetime = self.video_success_body.copy()
        video_invalid_datetime['datetime'] = 'invalid_datetime_format'
        response = self.app.post('/videos', json=video_invalid_datetime)

        self.assertEqual(response.status_code, 400)

    @mock.patch('app.repositories.video_repository.VideoRepository.save')
    def test_handle_duplicate_key_error(self, mock_save):
        mock_save.side_effect = DuplicateKeyError('test')
        response = self.app.post('/videos', json=self.video_success_body)

        self.assertEqual(mock_save.call_count, 1)
        self.assertEqual(response.status_code, 500)

    @mock.patch('app.repositories.video_repository.VideoRepository.find_all')
    def test_get_all_videos_success(self, mock_find):
        response = self.app.get('/videos')

        self.assertEqual(mock_find.call_count, 1)
        self.assertEqual(response.status_code, 200)

    def test_get_all_videos_with_invalid_limit(self):
        response = self.app.get('/videos?limit=not_integer')

        self.assertEqual(response.status_code, 400)

    def test_get_all_videos_with_invalid_offset(self):
        response = self.app.get('/videos?offset=not_integer')

        self.assertEqual(response.status_code, 400)



if __name__ == '__main__':
    unittest.main()
