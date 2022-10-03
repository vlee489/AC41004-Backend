import csv
import pymongo
import os
import certifi
ca = certifi.where()

URI = os.getenv("MONGOURI")
client = pymongo.MongoClient(URI, tlsCAFile=ca)
db = client.dev
items = []

with open("non_compliance.csv") as file:
    data = csv.DictReader(file)
    for row in data:
        resource_id = db.resources.find_one({"conversion.id": row["resource_id"]})
        rule_id = db.rules.find_one({"conversion.id": row["rule_id"]})
        items.append({
            "resource_id": resource_id["_id"],
            "rule_id": rule_id["_id"],
        })
    result = db.nonCompliances.insert_many(items)
    print(result)
