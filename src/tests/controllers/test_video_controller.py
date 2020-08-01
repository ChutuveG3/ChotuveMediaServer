import unittest

from mock import patch
from app import app
from pymongo.errors import DuplicateKeyError
from tests.clients import AppServerTestClient
from src.tests.clients import WebAdminTestClient


class TestVideoController(unittest.TestCase):
    video_success_body = {
        'file_name': 'file_name_test',
        'file_size': 1024,
        'download_url': 'http://url.com',
        'datetime': '2020-05-19T12:00:01'
    }
    video_error_body = {
        'file_name': 'file_name_test',
        'download_url': 'http://url.com',
        'datetime': '2020-05-19T12:00:01'
    }

    def setUp(self):
        # creates a test client
        app.test_client_class = AppServerTestClient
        self.app = app.test_client()
        app.test_client_class = WebAdminTestClient
        self.web_admin_client = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        self.web_admin_client.testing = True
        # mock auth validations
        self.patcher_server_validate = patch(
            'app.services.auth_service.AuthService.validate_app_server',
            return_value=True
        )
        self.patcher_admin_validate = patch(
            'app.services.auth_service.AuthService.validate_admin_token',
            return_value=True
        )
        self.mock_server_validate = self.patcher_server_validate.start()
        self.mock_admin_validate = self.patcher_admin_validate.start()

    def tearDown(self):
        # stop validation mock
        patch.stopall()

    @patch('app.repositories.video_repository.VideoRepository.save')
    def test_success_video_upload(self, mock_save):
        response = self.app.post('/videos', json=self.video_success_body)

        self.assertEqual(mock_save.call_count, 1)
        self.assertTrue('id' in response.json)
        self.assertEqual(response.status_code, 201)

    def test_validation_error_handle(self):
        response = self.app.post('/videos', json=self.video_error_body)

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

    def test_get_all_videos_with_invalid_page_number(self):
        response = self.app.get('/videos?page=not_integer')

        self.assertEqual(response.status_code, 400)

    def test_get_videos_with_invalid_id_raise_exception(self):
        response = self.app.get('/videos?id=1&id=not_integer')

        self.assertEqual(response.status_code, 400)

    @patch('app.repositories.video_repository.VideoRepository.find_by_id')
    @patch('app.repositories.video_repository.VideoRepository.delete')
    def test_delete_video_success(self, mock_delete, mock_find):
        # Delete video with id = 10.
        response = self.web_admin_client.delete('/videos/10')

        self.assertEqual(mock_delete.call_count, 1)
        self.assertEqual(mock_find.call_count, 1)
        self.assertEqual(response.status_code, 200)

    def test_delete_video_invalid_id(self):
        response = self.web_admin_client.delete('/videos/not_integer')

        self.assertEqual(response.status_code, 400)

    @patch('app.repositories.video_repository.VideoRepository.find_by_id')
    def test_get_all_videos_resp_headers(self, mock_find):
        response = self.app.get('/videos')

        self.assertEqual(mock_find.call_count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Access-Control-Allow-Origin' in response.headers)
        self.assertTrue('Access-Control-Allow-Headers' in response.headers)
        self.assertTrue('Access-Control-Allow-Methods' in response.headers)


if __name__ == '__main__':
    unittest.main()
