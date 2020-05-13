
class VideoRepository(object):
    def __init__(self):
        from .. import db
        self.video_collection = db.videos

    def save(self, video):
        self.video_collection.insert_one(video.to_mongo())
