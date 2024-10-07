from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import os
from jaeger_client import Config
from flask_opentracing import FlaskTracing

app = Flask(__name__)

# Jaeger configuration
def init_tracer():
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
    return config.initialize_tracer()

tracer = init_tracer()
tracing = FlaskTracing(tracer, True, app)

# Use environment variables for configuration
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/flaskapi")
mongo = PyMongo(app)

@app.route("/")
def hello():
    with tracer.start_span('hello') as span:
        span.set_tag('http.method', request.method)
        return jsonify({"message": "Welcome to the Flask API with MongoDB!"})

@app.route("/api/items", methods=["GET"])
def get_items():
    with tracer.start_span('get_items') as span:
        span.set_tag('http.method', request.method)
        items = list(mongo.db.items.find())
        return jsonify({"items": [{**item, "_id": str(item["_id"])} for item in items]})

@app.route("/api/items", methods=["POST"])
def add_item():
    with tracer.start_span('add_item') as span:
        span.set_tag('http.method', request.method)
        item = request.json.get("item")
        if not item:
            return jsonify({"error": "Invalid item"}), 400
        result = mongo.db.items.insert_one({"name": item})
        return jsonify({"message": "Item added successfully", "id": str(result.inserted_id)}), 201

@app.route("/api/items/<item_id>", methods=["GET"])
def get_item(item_id):
    with tracer.start_span('get_item') as span:
        span.set_tag('http.method', request.method)
        span.set_tag('item_id', item_id)
        item = mongo.db.items.find_one({"_id": ObjectId(item_id)})
        if item:
            return jsonify({**item, "_id": str(item["_id"])})
        return jsonify({"error": "Item not found"}), 404

@app.route("/api/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    with tracer.start_span('update_item') as span:
        span.set_tag('http.method', request.method)
        span.set_tag('item_id', item_id)
        item = request.json.get("item")
        if not item:
            return jsonify({"error": "Invalid item"}), 400
        result = mongo.db.items.update_one({"_id": ObjectId(item_id)}, {"$set": {"name": item}})
        if result.modified_count:
            return jsonify({"message": "Item updated successfully"})
        return jsonify({"error": "Item not found"}), 404

@app.route("/api/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    with tracer.start_span('delete_item') as span:
        span.set_tag('http.method', request.method)
        span.set_tag('item_id', item_id)
        result = mongo.db.items.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count:
            return jsonify({"message": "Item deleted successfully"})
        return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)