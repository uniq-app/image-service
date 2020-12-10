from bson import ObjectId
from bson.errors import InvalidId


class NoResultFound(Exception):
    pass


class Model(dict):
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    @property
    def id(self):
        return str(self._id)

    def save(self):
        if not self._id:
            self.collection.insert(self)
        else:
            self.collection.update(
                {"_id": ObjectId(self._id)}, self)

    def reload(self):
        if self._id:
            try:
                res = self.collection.find_one({"_id": self._id})
                self.update(res)
            except (InvalidId, TypeError):
                raise NoResultFound(f"No result was found with id: {self._id}")

    def remove(self):
        if self._id:
            try:
                self.collection.remove({"_id": self._id})
                self.clear()
            except InvalidId:
                raise NoResultFound(f"No result was found with id: {self._id}")
