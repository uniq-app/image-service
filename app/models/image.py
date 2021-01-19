from datetime import datetime as dt, timezone as tz
from uuid import uuid4


class Image:
    def __init__(self, filename: str, extension: str, created: str = None, _id: str = None, thumbnail_task: str = None):
        self._id = _id or uuid4().hex
        self.filename = filename
        self.extension = extension
        self.created = created or str(dt.utcnow().replace(microsecond=0).replace(tzinfo=tz.utc).isoformat())
        self.thumbnail_task = thumbnail_task

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def as_dict(self) -> dict:
        return {
            '_id': self._id,
            'filename': self.filename,
            'extension': self.extension,
            'created': self.created,
            'thumbnail_task': self.thumbnail_task
        }
