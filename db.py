from flask import Flask, request, json, Response
from pymongo import MongoClient
from bson import json_util


class DB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        db = "vendors_db"
        collection = "vendors_db"
        self.db = self.client[db]
        self.collection = self.db[collection]

    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def create(self, vendor):
        response = self.collection.insert_one(vendor)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}

        return output

    def update(self, id, data):
        return self.collection.find_one_and_update(filter={"_id": id},
                                                   update=data,
                                                   return_document=True)

    def get_all(self):
        data = self.collection.find().limit(20)
        return json.loads(json_util.dumps(data))

    def get(self, vendor_id):
        return self.collection.find_one({"_id": vendor_id})

    def delete(self, vendor_id):
        self.collection.delete_one({"_id": vendor_id})
        return


if __name__ == "__main__":
    data = {
        "database": "NipunDb",
        "collection": "people",
    }

    mongo_obj = DB(data)
    print(json.dumps(mongo_obj.read(), indent=4))
