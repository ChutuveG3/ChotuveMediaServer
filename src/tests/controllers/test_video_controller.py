import unittest

from mock import Mock, patch
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

    @patch('app.repositories.video_repository.VideoRepository.save')
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

    @patch('app.repositories.video_repository.VideoRepository.save')
    def test_handle_duplicate_key_error(self, mock_save):
        mock_save.side_effect = DuplicateKeyError('test')
        response = self.app.post('/videos', json=self.video_success_body)

        self.assertEqual(mock_save.call_count, 1)
        self.assertEqual(response.status_code, 500)

    @patch('app.repositories.video_repository.VideoRepository.find_by_id')
    def test_get_all_videos_success(self, mock_find):
        response = self.app.get('/videos?id=1&id=2')

        self.assertEqual(mock_find.call_count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('total' in response.headers)

    def test_get_all_videos_with_invalid_limit(self):
        response = self.app.get('/videos?limit=not_integer')

        self.assertEqual(response.status_code, 400)

    def test_get_all_videos_with_invalid_offset(self):
        response = self.app.get('/videos?offset=not_integer')

        self.assertEqual(response.status_code, 400)

    def test_get_videos_with_invalid_id_raise_exception(self):
        response = self.app.get('/videos?id=1&id=not_integer')

        self.assertEqual(response.status_code, 400)

    @patch('app.repositories.video_repository.VideoRepository.find_by_id')
    @patch('app.repositories.video_repository.VideoRepository.delete')
    @patch('requests.delete')
    def test_delete_video_success(self, mock_app_req, mock_delete, mock_find):
        # Set up delete req mock.
        mock_app_req.return_value = Mock(status_code=200, json=lambda: {"message": "ok"})
        # Delete video with id = 10.
        response = self.app.delete('/videos/10')

        self.assertEqual(mock_delete.call_count, 1)
        self.assertEqual(mock_find.call_count, 1)
        self.assertEqual(mock_app_req.call_count, 1)
        self.assertEqual(response.status_code, 200)

    def test_delete_video_invalid_id(self):
        response = self.app.delete('/videos/not_integer')

        self.assertEqual(response.status_code, 400)

    @patch('app.repositories.video_repository.VideoRepository.find_by_id')
    @patch('requests.delete')
    def test_delete_video_app_server_error(self, mock_app_req, mock_find):
        # Set up delete req mock: video not found.
        mock_app_req.return_value = Mock(status_code=404, json=lambda: {"error": "not found"})
        # Delete video with id = 10.
        response = self.app.delete('/videos/10')

        self.assertEqual(mock_app_req.call_count, 1)
        self.assertEqual(mock_find.call_count, 1)
        self.assertEqual(response.status_code, 402)


if __name__ == '__main__':
    unittest.main()
