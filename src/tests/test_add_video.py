import unittest
from src.app.models.video import Video


class TestVideoModel(unittest.TestCase):
    def test_to_default_datetime(self):
        video = Video(file_name='file_name_test')
        self.assertIsNotNone(video.datetime)


if __name__ == '__main__':
    unittest.main()
