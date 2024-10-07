import requests

BASE_URL = "http://localhost:5000"

def test_root():
    url = BASE_URL
    try:
        response = requests.get(url)
        print(f"Root Status Code: {response.status_code}")
        print(f"Root Response Content: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while testing root: {e}")

def test_add_item():
    url = f"{BASE_URL}/api/items"
    data = {
        "item": "Test Item"
    }
    
    try:
        response = requests.post(url, json=data)
        
        print(f"Add Item Status Code: {response.status_code}")
        print(f"Add Item Response Content: {response.text}")
        
        if 'application/json' in response.headers.get('Content-Type', ''):
            try:
                json_response = response.json()
                print(f"JSON Response: {json_response}")
            except requests.exceptions.JSONDecodeError:
                print("Response is not valid JSON")
        else:
            print("Response is not JSON")
        
        if response.status_code == 201:
            print("Item added successfully!")
        else:
            print(f"Failed to add item. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while adding item: {e}")

if __name__ == "__main__":
    test_root()
    print("\n---\n")
    test_add_item()