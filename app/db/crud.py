from bson import ObjectId
from app.db.database import collection


def insert_document(document: dict):
    """insert one documnet into default collection and returns id of inserted document"""

    data = collection.insert_one(document)
    return data.inserted_id


def insert_documents(documents: list[dict]):
    """insert multiple documnet into default collection and returns id of inserted document"""

    data = collection.insert_many(documents)
    return data.inserted_ids


def get_document(id: str):
    """get one documnet from default collection with specified '_id'"""

    data = collection.find_one({"_id": ObjectId(id)}, {"_id": 0})
    return data


def get_all_documents():
    """get all documnets from default collection without '_id' of document"""

    data = collection.find({}, {"_id": 0})
    return data
