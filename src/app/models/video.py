import datetime
from mongoengine import *

def _not_empty(val):
    if not val:
        raise ValidationError()


class VideoModel(Document):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate()

    _id = IntField()
    file_name = StringField(validation=_not_empty, required=True)
    file_size = IntField(validation=_not_empty, required=True,  min_value=0)
    download_url = StringField(validation=_not_empty, required=True)
    datetime = DateTimeField(default=datetime.datetime.utcnow)

