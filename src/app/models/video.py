from mongoengine import *


class Video(Document):
    file_name = StringField()
    file_size = IntField()
    download_url = StringField()
    datetime = DateTimeField()
