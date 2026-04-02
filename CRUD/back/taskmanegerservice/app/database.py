from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["taskmanager"]
tasks_collection = db["tasks"]
users_collection = db["users"]