from behave import given, when, then
import json

@when('I add a new item with name "{item_name}"')
def add_new_item(context, item_name):
    context.response = context.client.post('/api/items', json={'item': item_name})

@then('the response status code should be {status_code:d}')
def check_status_code(context, status_code):
    assert context.response.status_code == status_code

@then('the response should contain "{text}"')
def check_response_content(context, text):
    assert text in context.response.get_data(as_text=True)

@given('there are {count:d} items in the database')
def add_items_to_database(context, count):
    for i in range(count):
        context.db.items.insert_one({'name': f'Item {i+1}'})

@when('I request all items')
def request_all_items(context):
    context.response = context.client.get('/api/items')

@then('the response should contain {count:d} items')
def check_item_count(context, count):
    data = json.loads(context.response.get_data(as_text=True))
    assert len(data['items']) == count

@given('there is an item with name "{item_name}" in the database')
def add_specific_item_to_database(context, item_name):
    context.db.items.insert_one({'name': item_name})

@when('I request the item "{item_name}"')
def request_specific_item(context, item_name):
    item = context.db.items.find_one({'name': item_name})
    context.response = context.client.get(f'/api/items/{item["_id"]}')

@when('I update the item "{old_name}" to "{new_name}"')
def update_item(context, old_name, new_name):
    item = context.db.items.find_one({'name': old_name})
    context.response = context.client.put(f'/api/items/{item["_id"]}', json={'item': new_name})

@when('I delete the item "{item_name}"')
def delete_item(context, item_name):
    item = context.db.items.find_one({'name': item_name})
    context.response = context.client.delete(f'/api/items/{item["_id"]}')

@when('I request a non-existent item')
def request_non_existent_item(context):
    context.response = context.client.get('/api/items/000000000000000000000000')