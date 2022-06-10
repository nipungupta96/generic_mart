from flask import Flask, request, json, Response
from pymongo import MongoClient


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

    def create(self, data):
        print("Writing Data")
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}

        return output

    def update(self, data):
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

    def get_all(self):
        return self.collection.find().limit(20)

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
