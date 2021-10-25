import pymongo


class Mongo:
    def __init__(self, host=None, port=None, user=None, pwd=None):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.client = pymongo.MongoClient(self.host, self.port)

    def connection(self, database):
        db = self.client["admin"]
        if self.pwd is not None:
            db.authenticate(self.user, self.pwd, mechanism="MONGODB-CR")
        db = self.client[database]
        return db