import unittest

from src.app.models.video import Video


class TestVideoModel(unittest.TestCase):
    def test_video_filename(self):
        video = Video(file_name='file_name_test')
        self.assertEqual(video.file_name, None)
        self.assertEqual(video.datetime, None)
        self.assertEqual(video.download_url, None)


if __name__ == '__main__':
    unittest.main()
