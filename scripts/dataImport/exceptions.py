import csv
import pymongo
from datetime import datetime, timedelta
from bson import ObjectId
import certifi
import os
ca = certifi.where()

URI = os.getenv("MONGOURI")
client = pymongo.MongoClient(URI, tlsCAFile=ca)
db = client.dev
items = []

with open("exception.csv") as file:
    data = csv.DictReader(file)
    for row in data:
        rule_id = db.rules.find_one({"conversion.id": row["rule_id"]})
        review_date = datetime.strptime(row["review_date"][:-6], "%Y-%m-%d %H:%M:%S.%f") - timedelta(hours=1)
        last_updated = datetime.strptime(row["last_updated"][:-6], "%Y-%m-%d %H:%M:%S.%f") - timedelta(hours=1)
        items.append({
            "customer_id": ObjectId("633ad262a938b45d958ae766"),
            "rule_id": rule_id["_id"],
            "last_updated_by": ObjectId("6336e3470bb7de25d225190b"),
            "exception_value": row["exception_value"],
            "justification": row["justification"],
            "review_date": review_date,
            "last_updated": last_updated,
            "conversion": {
                "id": row["exception_id"]
            }
        })
    result = db.exceptions.insert_many(items)
    print(result)
