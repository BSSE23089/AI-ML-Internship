from pymongo import MongoClient
from .model import Model
from bson import ObjectId

client = MongoClient("mongodb+srv://itsshizashahbaz_db_user:Va4VoYFvvZsxCSXh@cluster0.hx0sjxz.mongodb.net/?appName=Cluster0")
database = client["ModelRegistry"]
collection = database["Model"]


def get_models():
    models = list(collection.find()) 
    for m in models:
        m["_id"] = str(m["_id"]) 
    return {"message": "models retrieved!!", "models": models}

def post_model(model: Model):
    result = collection.insert_one(model.model_dump())

    return {
        "message": "model added!!",
        "inserted_id": str(result.inserted_id)
    }

def delete_model(model_id: str):
    result = collection.delete_one({"_id": ObjectId(model_id)})
    return {'message:': 'model deleted!!'}

def update_model(model_id: str, model: Model):
    result = collection.update_one({"_id": ObjectId(model_id)}, {"$set": model.model_dump()})
    return {'message:': 'model updated!!'}


