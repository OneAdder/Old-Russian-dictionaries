import json
from pymongo import MongoClient

client = MongoClient('localhost', 33017)

db = client.old_russian
coll = db.or_dictionaries
for col in coll.find():
    print(col)
    break

with open('matched.json', 'r', encoding='utf-8') as f:
    matched = json.load(f)

for_mongo = []

for key, value in matched.items():
    value['unified_lemma'] = key
    for_mongo.append(value)

print(for_mongo[0])

coll.insert_many(for_mongo)




