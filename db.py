from flask import Flask, request, json, Response
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId


def handle_bson(func):
    def wrapper(*args):
        return json.loads(json_util.dumps(func(*args)))
    return wrapper


class DB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        db = "vendors_db"
        collection = "vendors_db"
        self.db = self.client[db]
        self.collection = self.db[collection]

    @handle_bson
    def create(self, vendor):
        response = self.collection.insert_one(vendor)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}

        return output

    @handle_bson
    def update(self, vendor_id, data):
        return self.collection.find_one_and_update(filter={"_id": ObjectId(vendor_id)},
                                                   update=data,
                                                   return_document=True)

    @handle_bson
    def get_all(self):
        return self.collection.find().limit(20)

    @handle_bson
    def get(self, vendor_id):
        return self.collection.find_one({"_id": ObjectId(vendor_id)})

    def delete(self, vendor_id):
        self.collection.delete_one({"_id": vendor_id})
        return
