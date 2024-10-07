"""
Flask application for managing items with MongoDB backend and Jaeger tracing.
"""

from typing import Dict, List, Optional
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import os
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from opentracing.propagation import Format

app = Flask(__name__)

def init_tracer() -> FlaskTracing:
    """
    Initialize Jaeger tracer.

    Returns:
        FlaskTracing: Configured Flask tracing object.
    """
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': os.environ.get('JAEGER_AGENT_HOST', 'localhost'),
                'reporting_port': int(os.environ.get('JAEGER_AGENT_PORT', 6831)),
            },
            'logging': True,
        },
        service_name='flask-api',
    )
    return FlaskTracing(config.initialize_tracer(), True, app)

tracing = init_tracer()

# Use environment variables for configuration
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/flaskapi")
mongo = PyMongo(app)

@app.route("/")
def hello() -> Dict[str, str]:
    """
    Root endpoint.

    Returns:
        Dict[str, str]: Welcome message.
    """
    with tracing.tracer.start_span('hello') as span:
        span.set_tag('http.method', request.method)
        return jsonify({"message": "Welcome to the Flask API with MongoDB!"})

@app.route("/api/items", methods=["GET"])
def get_items() -> Dict[str, List[Dict]]:
    """
    Get all items.

    Returns:
        Dict[str, List[Dict]]: List of all items.
    """
    with tracing.tracer.start_span('get_items') as span:
        span.set_tag('http.method', request.method)
        items = list(mongo.db.items.find())
        return jsonify({"items": [{**item, "_id": str(item["_id"])} for item in items]})

@app.route("/api/items", methods=["POST"])
def add_item() -> tuple[Dict[str, str], int]:
    """
    Add a new item.

    Returns:
        tuple[Dict[str, str], int]: Message confirming item addition and status code.
    """
    with tracing.tracer.start_span('add_item') as span:
        span.set_tag('http.method', request.method)
        item = request.json.get("item")
        if not item:
            return jsonify({"error": "Invalid item"}), 400
        result = mongo.db.items.insert_one({"name": item})
        return jsonify({"message": "Item added successfully", "id": str(result.inserted_id)}), 201

@app.route("/api/items/<item_id>", methods=["GET"])
def get_item(item_id: str) -> tuple[Dict, int]:
    """
    Get a specific item.

    Args:
        item_id (str): The ID of the item to retrieve.

    Returns:
        tuple[Dict, int]: Item data and status code.
    """
    with tracing.tracer.start_span('get_item') as span:
        span.set_tag('http.method', request.method)
        span.set_tag('item_id', item_id)
        item = mongo.db.items.find_one({"_id": ObjectId(item_id)})
        if item:
            return jsonify({**item, "_id": str(item["_id"])}), 200
        return jsonify({"error": "Item not found"}), 404

@app.route("/api/items/<item_id>", methods=["PUT"])
def update_item(item_id: str) -> tuple[Dict[str, str], int]:
    """
    Update an existing item.

    Args:
        item_id (str): The ID of the item to update.

    Returns:
        tuple[Dict[str, str], int]: Message confirming update and status code.
    """
    with tracing.tracer.start_span('update_item') as span:
        span.set_tag('http.method', request.method)
        span.set_tag('item_id', item_id)
        item = request.json.get("item")
        if not item:
            return jsonify({"error": "Invalid item"}), 400
        result = mongo.db.items.update_one({"_id": ObjectId(item_id)}, {"$set": {"name": item}})
        if result.modified_count:
            return jsonify({"message": "Item updated successfully"}), 200
        return jsonify({"error": "Item not found"}), 404

@app.route("/api/items/<item_id>", methods=["DELETE"])
def delete_item(item_id: str) -> tuple[Dict[str, str], int]:
    """
    Delete an item.

    Args:
        item_id (str): The ID of the item to delete.

    Returns:
        tuple[Dict[str, str], int]: Message confirming deletion and status code.
    """
    with tracing.tracer.start_span('delete_item') as span:
        span.set_tag('http.method', request.method)
        span.set_tag('item_id', item_id)
        result = mongo.db.items.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count:
            return jsonify({"message": "Item deleted successfully"}), 200
        return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)