from pymongo import ReturnDocument

from src.app.models import VideoModel


class VideoRepository(object):
    VIDEO_COUNTER_ID = 'videoid'
    SEQ_NUMBER_ID = 'seq'
    INCREMENT = 1

    def __init__(self):
        from .. import db
        self.video_collection = db.videos

    def save(self, video):
        video._id = self.__get_next_id()
        self.video_collection.insert_one(video.to_mongo())

    def find_all(self, limit=0):
        '''
        :param limit: limit count return values. A limit value of 0 (i.e. .limit(0)) is
        equivalent to setting no limit.
        :return: list of Videos. [] on empty result.
        '''
        result = self.video_collection.find().limit(limit)

        return [self.__load(data) for data in result]

    def __load(self, data):
        return VideoModel(**data)

    def __get_next_id(self):
        '''
        Increment the sequence number in 1. If videoid matches no existing document,
        MongoDB will refuse to insert a new document, else only update.
        :return: next video id
        '''
        from .. import db
        ret = db.counters.find_one_and_update(
            {'_id': self.VIDEO_COUNTER_ID},
            {'$inc': {self.SEQ_NUMBER_ID: self.INCREMENT}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        return ret[self.SEQ_NUMBER_ID]
