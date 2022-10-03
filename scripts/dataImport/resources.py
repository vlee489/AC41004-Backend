import csv
import pymongo
from datetime import datetime, timedelta
from bson import ObjectId
import json
import certifi
import os
ca = certifi.where()

URI = os.getenv("MONGOURI")

resource_map = {
    1: ObjectId("633ad142a938b45d958ae754"),
    2: ObjectId("633ad142a938b45d958ae755"),
    3: ObjectId("633ad142a938b45d958ae756"),
    4: ObjectId("633ad142a938b45d958ae757"),
    5: ObjectId("633ad142a938b45d958ae758"),
    6: ObjectId("633ad142a938b45d958ae759"),
    7: ObjectId("633ad142a938b45d958ae75a"),
    10: ObjectId("633ad142a938b45d958ae75b"),
    11: ObjectId("633ad142a938b45d958ae75c"),
    12: ObjectId("633ad142a938b45d958ae75d"),
}

client = pymongo.MongoClient(URI, tlsCAFile=ca)
db = client.dev
items = []

with open("resource.csv") as file:
    data = csv.DictReader(file)
    for row in data:
        metadata = json.loads(row["resource_metadata"])
        last_updated = datetime.strptime(row["last_updated"][:-6], "%Y-%m-%d %H:%M:%S.%f") - timedelta(hours=1)
        type_id = resource_map.get(int(row["resource_type_id"]))
        items.append({
            "reference": row["resource_ref"],
            "account_id": ObjectId("633ad7aca938b45d958ae772"),
            "type_id": type_id,
            "name": row["resource_name"],
            "last_updated": last_updated,
            "conversion": {
                "id": row["resource_id"]
            },
            "metadata": metadata
        })
    result = db.resources.insert_many(items)
    print(result)
