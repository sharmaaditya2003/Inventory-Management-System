from cryptography.fernet import Fernet
import os
from product_operations import add_product, update_product, remove_product, search_product, sort_products, filter_products
from stock_operations import view_stock
from reports import sales_report, inventory_turnover_report, financial_report, top_products_report, low_stock_report

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
                add_product()
            elif choice == '2':
                update_product()
            elif choice == '3':
                remove_product()
            elif choice == '4':
                search_product()
            elif choice == '5':
                sort_products()
            elif choice == '6':
                filter_products()
            elif choice == '7':
                view_stock()
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
            sales_report()
        elif report_choice == '2':
            inventory_turnover_report()
        elif report_choice == '3':
            financial_report()
        elif report_choice == '4':
            top_products_report()
        elif report_choice == '5':
            low_stock_report()
        elif report_choice == '6':
            return
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    app = InventoryManagementApp()
    app.execute_application()
