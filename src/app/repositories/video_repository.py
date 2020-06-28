from pymongo import ReturnDocument

from src.app.exceptions import VideoNotFoundError
from src.app.models import VideoModel


class VideoRepository(object):
    VIDEO_COUNTER_ID = 'videoid'
    SEQ_NUMBER_ID = 'seq'
    INCREMENT = 1

    def __init__(self):
        from .. import db
        self.video_collection = db.videos

    def save(self, video):
        video._id = self._get_next_id()
        self.video_collection.insert_one(video.to_mongo())

    def find_by_id(self, id_list=[], limit=0, offset=0):
        '''
        :param id_list: filter by video id's.
        :param limit: limit count return values. A limit value of 0 (i.e. .limit(0)) is
        equivalent to setting no limit.
        :param offset: skip offset videos. A offset value of 0 (i.e. .limit(0)) is
        equivalent to setting no offset.
        :return: list of Videos. Raise VideoNotFoundError when result lt id´s.
        '''
        query = {'_id': {'$in': id_list}} if id_list else {}
        result = self.video_collection.find(query, limit=limit, skip=offset)
        if result.count(True) < len(id_list):
            raise VideoNotFoundError('videos not found')

        return [self._load(data) for data in result]

    def _load(self, data):
        return VideoModel(**data)

    def _get_next_id(self):
        '''
        Increment the sequence number in 1. If videoid matches no existing document,
        MongoDB will refuse to insert a new document, else only up date.
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
