import pymongo
from pymongo import MongoClient

client = MongoClient()

db = client["Authchain"]


users = db["users"]
services = db["services"]

#services.create_index([("fuck", pymongo.DESCENDING)], unique=True)
result = services.insert_one({"life" : 6, "balls" : "wow"})
#print (result.inserted_id)

for document in services.find():
    print(document)
