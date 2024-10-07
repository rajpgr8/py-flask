from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import os

app = Flask(__name__)

# Use environment variables for configuration
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/flaskapi")
mongo = PyMongo(app)

@app.route("/")
def hello():
    return jsonify({"message": "Welcome to the Flask API with MongoDB!"})

@app.route("/api/items", methods=["GET"])
def get_items():
    items = list(mongo.db.items.find())
    return jsonify({"items": [{**item, "_id": str(item["_id"])} for item in items]})

@app.route("/api/items", methods=["POST"])
def add_item():
    item = request.json.get("item")
    if not item:
        return jsonify({"error": "Invalid item"}), 400
    result = mongo.db.items.insert_one({"name": item})
    return jsonify({"message": "Item added successfully", "id": str(result.inserted_id)}), 201

@app.route("/api/items/<item_id>", methods=["GET"])
def get_item(item_id):
    item = mongo.db.items.find_one({"_id": ObjectId(item_id)})
    if item:
        return jsonify({**item, "_id": str(item["_id"])})
    return jsonify({"error": "Item not found"}), 404

@app.route("/api/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    item = request.json.get("item")
    if not item:
        return jsonify({"error": "Invalid item"}), 400
    result = mongo.db.items.update_one({"_id": ObjectId(item_id)}, {"$set": {"name": item}})
    if result.modified_count:
        return jsonify({"message": "Item updated successfully"})
    return jsonify({"error": "Item not found"}), 404

@app.route("/api/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    result = mongo.db.items.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count:
        return jsonify({"message": "Item deleted successfully"})
    return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)