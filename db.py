from pymongo import MongoClient

MONGO_URI = "mongodb+srv://clinic:b9moA024SGH2HqOf@clinic.ni0hhkz.mongodb.net/?appName=clinic"

client = MongoClient(MONGO_URI)

db = client["clinic"]

appointments = db["appointments"]