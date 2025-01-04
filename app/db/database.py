import pymongo
from app.config.settings import settings

client = pymongo.MongoClient(settings.MONGODB_CONNECTION_STRING)

db = client[settings.MONGODB_DATABASE]

collection = db[settings.MONGODB_COLLECTION]
