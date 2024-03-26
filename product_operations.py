from models import Product
import json

def load_inventory(inventory_file='inventory.json'):
    try:
        with open(inventory_file, 'r') as file:
            inventory_data = json.load(file)
    except FileNotFoundError:
        inventory_data = []

    inventory = []
    for product_data in inventory_data:
        product = Product(
            product_data.get('product_id'),
            product_data.get('product_name'),
            product_data.get('quantity'),
            product_data.get('price'),
            product_data.get('category'),
            product_data.get('brand', ''),
            product_data.get('sales', 0)
        )
        inventory.append(product)

    return inventory

def save_inventory(inventory, inventory_file='inventory.json'):
    inventory_data = [product.__dict__ for product in inventory]
    with open(inventory_file, 'w') as file:
        json.dump(inventory_data, file, indent=2)

def add_product():
    inventory = load_inventory()

    try:
        product_data = {
            'product_id': len(inventory) + 1,
            'product_name': input("Enter product name: "),
            'quantity': int(input("Enter quantity: ")),
            'price': float(input("Enter price: ")),
            'category': input("Enter category: "),
            'brand': input("Enter brand: "),
        }
    except ValueError:
        print("Invalid input. Please enter a valid quantity and price.")
        return

    new_product = Product(**product_data)
    inventory.append(new_product)

    save_inventory(inventory)
    print("Product added successfully!")

def update_product():
    inventory = load_inventory()

    product_id = int(input("Enter product ID to update: "))
    for product in inventory:
        if product.product_id == product_id:
            try:
                quantity_sold = int(input("Enter quantity sold: "))
                product.update_sales(quantity_sold)
                product.quantity -= quantity_sold
            except ValueError:
                print("Invalid input. Please enter a valid quantity.")
                return
            save_inventory(inventory)
            print("Product updated successfully!")
            return

    print("Product not found.")


def remove_product():
    inventory = load_inventory()

    product_id = int(input("Enter product ID to remove: "))
    
    # Use a list comprehension to filter out the product to be removed
    inventory = [product for product in inventory if product.product_id != product_id]

    save_inventory(inventory)
    print("Product removed successfully!")
def search_product():
    inventory = load_inventory()

    keyword = input("Enter keyword to search: ")

    matching_products = [product for product in inventory if keyword.lower() in product.product_name.lower()]

    if matching_products:
        print("\nMatching Products:")
        for product in matching_products:
            print(f"Product ID: {product.product_id}, Name: {product.product_name}, Quantity: {product.quantity}, Price: ${product.price:.2f}")
    else:
        print("No matching products found.")

def sort_products():
    inventory = load_inventory()

    print("\nSort Options:")
    print("1. Sort by Product Name")
    print("2. Sort by Quantity")
    print("3. Sort by Price")
    print("4. Sort by Brand")
    print("5. Back to Main Menu")

    sort_option = input("Enter your choice (1-5): ")

    if sort_option == '5':
        return

    reverse_order = input("Sort in descending order? (y/n): ").lower() == 'y'

    if sort_option == '1':
        sorted_inventory = sorted(inventory, key=lambda x: x.product_name.lower(), reverse=reverse_order)
    elif sort_option == '2':
        sorted_inventory = sorted(inventory, key=lambda x: x.quantity, reverse=reverse_order)
    elif sort_option == '3':
        sorted_inventory = sorted(inventory, key=lambda x: x.price, reverse=reverse_order)
    elif sort_option == '4':
        sorted_inventory = sorted(inventory, key=lambda x: x.brand.lower(), reverse=reverse_order)
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
        return

    print("\nSorted Inventory:")
    for product in sorted_inventory:
        print(f"Product ID: {product.product_id}, Name: {product.product_name}, Quantity: {product.quantity}, Price: ${product.price:.2f}, Brand: {product.brand}")

    input("Press Enter to continue...")
def filter_products():
    inventory = load_inventory()

    category_filter = input("Enter category to filter (press Enter to skip): ").lower()
    brand_filter = input("Enter brand to filter (press Enter to skip): ").lower()

    filtered_products = []

    for product in inventory:
        category_match = category_filter == '' or category_filter == product.category.lower()
        brand_match = brand_filter == '' or brand_filter == product.brand.lower()

        if category_match and brand_match:
            filtered_products.append(product)

    if filtered_products:
        print("\nFiltered Products:")
        for product in filtered_products:
            print(f"Product ID: {product.product_id}, Name: {product.product_name}, Quantity: {product.quantity}, Price: ${product.price:.2f}, Category: {product.category}, Brand: {product.brand}")
    else:
        print("No products found matching the specified filters.")