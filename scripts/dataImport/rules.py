import csv
import pymongo
from bson import ObjectId
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

with open("rule.csv") as file:
    data = csv.DictReader(file)
    for row in data:
        type_id = resource_map.get(int(row["resource_type_id"]))
        items.append({
            "description": row["rule_description"],
            "type_id": type_id,
            "name": row["rule_name"],
            "conversion": {
                "id": row["rule_id"]
            },
        })
    result = db.rules.insert_many(items)
    print(result)
