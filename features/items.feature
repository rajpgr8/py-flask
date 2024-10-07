Feature: Item Management
  As an API user
  I want to manage items
  So that I can keep track of my inventory

  Scenario: Add a new item
    When I add a new item with name "Test Item"
    Then the response status code should be 201
    And the response should contain "Item added successfully"

  Scenario: Get all items
    Given there are 2 items in the database
    When I request all items
    Then the response status code should be 200
    And the response should contain 2 items

  Scenario: Get a specific item
    Given there is an item with name "Specific Item" in the database
    When I request the item "Specific Item"
    Then the response status code should be 200
    And the response should contain "Specific Item"

  Scenario: Update an item
    Given there is an item with name "Old Item" in the database
    When I update the item "Old Item" to "New Item"
    Then the response status code should be 200
    And the response should contain "Item updated successfully"

  Scenario: Delete an item
    Given there is an item with name "To Be Deleted" in the database
    When I delete the item "To Be Deleted"
    Then the response status code should be 200
    And the response should contain "Item deleted successfully"

  Scenario: Get a non-existent item
    When I request a non-existent item
    Then the response status code should be 404
    And the response should contain "Item not found"