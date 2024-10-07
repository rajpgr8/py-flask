from app import app, mongo
from flask.testing import FlaskClient
from pymongo import MongoClient
import os

def before_all(context):
    context.client = app.test_client()
    context.mongo_client = MongoClient(os.environ.get("MONGO_URI", "mongodb://mongodb:27017/testdb"))
    context.db = context.mongo_client.get_database()

def before_scenario(context, scenario):
    context.db.items.delete_many({})  # Clear the database before each scenario

def after_all(context):
    context.mongo_client.close()