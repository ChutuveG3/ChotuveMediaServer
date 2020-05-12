from mongoengine import *
import datetime

def _not_empty(val):
    if not val:
        raise ValidationError()



class Video(Document):
    file_name = StringField(validation=_not_empty)
    file_size = IntField(validation=_not_empty, min_value=0)
    download_url = StringField(validation=_not_empty)
    datetime = DateTimeField(validation=_not_empty, default=datetime.datetime.utcnow)
