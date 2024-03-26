from cryptography.fernet import Fernet
import json

class Product:
    def __init__(self, product_id, product_name, quantity, price, category, brand, sales=0):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
        self.category = category
        self.brand = brand
        self.sales = sales

    def update_sales(self, quantity_sold):
        self.sales += quantity_sold

class InventoryManagementApp:
    KEY_FILE = 'encryption_key.key'

    def generate_key(self):
        key = Fernet.generate_key()
        with open(self.KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        print("Encryption key generated. Please store it securely.")

    def get_key(self):
        try:
            with open(self.KEY_FILE, 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            return None

    def encrypt_data(self, data, key):
        cipher = Fernet(key)
        return cipher.encrypt(data.encode('utf-8'))

    def decrypt_data(self, encrypted_data, key):
        cipher = Fernet(key)
        return cipher.decrypt(encrypted_data).decode('utf-8')

    def execute_application(self):
        key = self.get_key()

        if key is None:
            self.generate_key()
            exit()

        user_key = input("Enter your encryption key: ")

        if user_key != key.decode('utf-8'):
            print("Incorrect encryption key. Exiting.")
            exit()

        self.run_application()

    def run_application(self):
        while True:
            print("\nOperations:")
            print("1. Add Product")
            print("2. Update Product")
            print("3. Remove Product")
            print("4. Search Product")
            print("5. Sort Products")
            print("6. Filter Products")
            print("7. View Stock")
            print("8. Generate Reports")
            print("9. Exit")

            choice = input("Enter your choice (1-9): ")

            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.update_product()
            elif choice == '3':
                self.remove_product()
            elif choice == '4':
                self.search_product()
            elif choice == '5':
                self.sort_products()
            elif choice == '6':
                self.filter_products()
            elif choice == '7':
                self.view_stock()
            elif choice == '8':
                self.generate_reports()
            elif choice == '9':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 9.")

    def generate_reports(self):
        print("\nSelect a report to generate:")
        print("1. Sales Report")
        print("2. Inventory Turnover Report")
        print("3. Financial Report")
        print("4. Top Products Report")
        print("5. Low Stock Report")
        print("6. Back to Main Menu")

        report_choice = input("Enter your choice (1-6): ")

        if report_choice == '1':
            self.sales_report()
        elif report_choice == '2':
            self.inventory_turnover_report()
        elif report_choice == '3':
            self.financial_report()
        elif report_choice == '4':
            self.top_products_report()
        elif report_choice == '5':
            self.low_stock_report()
        elif report_choice == '6':
            return
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

    def add_product(self):
        inventory = self.load_inventory()

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

        self.save_inventory(inventory)
        print("Product added successfully!")

    def update_product(self):
        inventory = self.load_inventory()

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
                self.save_inventory(inventory)
                print("Product updated successfully!")
                return

        print("Product not found.")

    def remove_product(self):
        inventory = self.load_inventory()

        product_id = int(input("Enter product ID to remove: "))
        inventory = [product for product in inventory if product.product_id != product_id]

        self.save_inventory(inventory)
        print("Product removed successfully!")

    def search_product(self):
        inventory = self.load_inventory()

        keyword = input("Enter keyword to search: ")

        matching_products = [product for product in inventory if keyword.lower() in product.product_name.lower()]

        if matching_products:
            print("\nMatching Products:")
            for product in matching_products:
                print(f"Product ID: {product.product_id}, Name: {product.product_name}, Quantity: {product.quantity}, Price: ${product.price:.2f}")
        else:
            print("No matching products found.")

    def sort_products(self):
        inventory = self.load_inventory()

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

    def filter_products(self):
        inventory = self.load_inventory()

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

    def sales_report(self):
        inventory = self.load_inventory()
    
        print("\nSales Report:")
        for product in inventory:
            total_quantity_sold = product.sales
            total_revenue = total_quantity_sold * product.price
        
            print(f"Product: {product.product_name}, Total Quantity Sold: {total_quantity_sold}, Total Revenue: ${total_revenue:.2f}")

    def inventory_turnover_report(self):
        inventory = self.load_inventory()
    
        print("\nInventory Turnover Report:")
        for product in inventory:
            turnover_rate = product.sales / product.quantity if product.quantity != 0 else 0
            print(f"Product: {product.product_name}, Turnover Rate: {turnover_rate:.2f} times per unit")

    def financial_report(self):
        inventory = self.load_inventory()

        total_revenue = sum(product.sales * product.price for product in inventory)
        total_cogs = sum(product.quantity * product.price for product in inventory)
        total_profit = total_revenue - total_cogs
    
        print("\nFinancial Report:")
        print(f"Total Revenue: ${total_revenue:.2f}")
        print(f"Total Cost of Goods Sold (COGS): ${total_cogs:.2f}")
        print(f"Total Profit: ${total_profit:.2f}")

    def top_products_report(self, sort_by='sales', num_top=5):
        inventory = self.load_inventory()
    
        sorted_inventory = sorted(inventory, key=lambda x: getattr(x, sort_by), reverse=True)[:num_top]
    
        print(f"\nTop Products Report (Sorted by {sort_by}):")
        for product in sorted_inventory:
            print(f"Product: {product.product_name}, {sort_by.capitalize()}: ${getattr(product, sort_by):.2f}")

    def low_stock_report(self, threshold=10):
        inventory = self.load_inventory()
    
        low_stock_products = [product for product in inventory if product.quantity < threshold]
    
        if not low_stock_products:
            print("\nNo products below the specified stock threshold.")
            return

        print(f"\nLow Stock Report (Threshold: {threshold}):")
        for product in low_stock_products:
            print(f"Product: {product.product_name}, Current Stock: {product.quantity}")

    def load_inventory(self, inventory_file='inventory.json'):
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

    def save_inventory(self, inventory, inventory_file='inventory.json'):
        inventory_data = [product.__dict__ for product in inventory]
        with open(inventory_file, 'w') as file:
            json.dump(inventory_data, file, indent=2)

if __name__ == "__main__":
    app = InventoryManagementApp()
    app.execute_application()
