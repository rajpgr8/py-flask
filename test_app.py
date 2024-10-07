import pytest
from flask import Flask
from flask.testing import FlaskClient
from app import app, mongo
import json
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import time
from bson import ObjectId

def wait_for_mongodb(uri, max_attempts=5, delay=1):
    client = MongoClient(uri)
    attempts = 0
    while attempts < max_attempts:
        try:
            client.admin.command('ismaster')
            return True
        except ServerSelectionTimeoutError:
            attempts += 1
            time.sleep(delay)
    return False

@pytest.fixture(scope='session')
def mongo_client():
    mongo_uri = 'mongodb://mongodb:27017/testdb'
    if not wait_for_mongodb(mongo_uri):
        pytest.fail("MongoDB is not available")
    return MongoClient(mongo_uri)

@pytest.fixture
def client(mongo_client):
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://mongodb:27017/testdb'
    with app.test_client() as client:
        with app.app_context():
            mongo_client.drop_database('testdb')
        yield client

def test_mongodb_connection(mongo_client):
    assert mongo_client.server_info()['ok'] == 1.0

def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == "Welcome to the Flask API with MongoDB!"

def test_add_item(client):
    response = client.post('/api/items', json={'item': 'Test Item'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Item added successfully'
    assert 'id' in data

def test_add_item_invalid_data(client):
    response = client.post('/api/items', json={})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Invalid item'

def test_get_items_empty(client):
    response = client.get('/api/items')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert len(data['items']) == 0

def test_get_items(client):
    client.post('/api/items', json={'item': 'Test Item 1'})
    client.post('/api/items', json={'item': 'Test Item 2'})
    
    response = client.get('/api/items')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert len(data['items']) == 2
    assert data['items'][0]['name'] == 'Test Item 1'
    assert data['items'][1]['name'] == 'Test Item 2'

def test_get_item(client):
    add_response = client.post('/api/items', json={'item': 'Test Item'})
    item_id = json.loads(add_response.data)['id']
    
    response = client.get(f'/api/items/{item_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Test Item'

def test_get_item_not_found(client):
    non_existent_id = str(ObjectId())
    response = client.get(f'/api/items/{non_existent_id}')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Item not found'

def test_update_item(client):
    add_response = client.post('/api/items', json={'item': 'Test Item'})
    item_id = json.loads(add_response.data)['id']
    
    response = client.put(f'/api/items/{item_id}', json={'item': 'Updated Test Item'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Item updated successfully'
    
    # Verify the item was updated
    get_response = client.get(f'/api/items/{item_id}')
    get_data = json.loads(get_response.data)
    assert get_data['name'] == 'Updated Test Item'

def test_update_item_not_found(client):
    non_existent_id = str(ObjectId())
    response = client.put(f'/api/items/{non_existent_id}', json={'item': 'Updated Test Item'})
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Item not found'

def test_update_item_invalid_data(client):
    add_response = client.post('/api/items', json={'item': 'Test Item'})
    item_id = json.loads(add_response.data)['id']
    
    response = client.put(f'/api/items/{item_id}', json={})
    assert response