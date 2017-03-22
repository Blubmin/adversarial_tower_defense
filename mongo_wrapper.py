import pymongo

class MongoWrapper:
    def __init__(self):
        self._db = pymongo.MongoClient().td

    def get_tower_data(self):
        try:
            return self._db.tower.find({})
        except:
            return None

    def save_tower_data(self, data):
            return self._db.tower.insert_many(data)

    def clear_collections(self):
        try:
            self._db.tower.delete({})
        finally:
            return None

