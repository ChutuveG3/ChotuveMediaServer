import datetime

import re
from mongoengine import *


def _not_empty(val):
    if not val:
        raise ValidationError()


class VideoModel(Document):
    URL_FORMAT_REGEX = re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}"
                                  r"\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate()

    _id = IntField()
    file_name = StringField(validation=_not_empty, required=True)
    file_size = IntField(validation=_not_empty, required=True, min_value=0)
    download_url = URLField(URL_FORMAT_REGEX, validation=_not_empty, required=True)
    datetime = DateTimeField(default=datetime.datetime.utcnow)
