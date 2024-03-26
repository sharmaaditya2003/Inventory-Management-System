import json

def load_inventory(inventory_file='inventory.json'):
    try:
        with open(inventory_file, 'r') as file:
            inventory = json.load(file)
    except FileNotFoundError:
        inventory = []

    return inventory

def view_stock():
    inventory = load_inventory()

    if not inventory:
        print("No products in the inventory.")
        return

    print("\nCurrent Stock:")
    for product in inventory:
        print(f"ID: {product['product_id']}, Name: {product['product_name']}, Quantity: {product['quantity']}, Price: {product['price']}, Category: {product['category']}")
