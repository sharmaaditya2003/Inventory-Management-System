from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from cryptography.fernet import Fernet
import json

from InventoHub import Product


class InventoryManagementApp(App):

    def build(self):
        # Initialize the key file
        self.KEY_FILE = 'encryption_key.key'
        self.initialize_key()

        # Main layout
        self.layout = BoxLayout(orientation='vertical')

        # Add buttons for each operation
        self.add_button("Add Product", self.add_product)
        self.add_button("Update Product", self.update_product)
        self.add_button("Remove Product", self.remove_product)
        self.add_button("Search Product", self.search_product)
        self.add_button("Sort Products", self.sort_products)
        self.add_button("Filter Products", self.filter_products)
        self.add_button("View Stock", self.view_stock)
        self.add_button("Generate Reports", self.generate_reports)
        self.add_button("Exit", self.stop)

        return self.layout

    def initialize_key(self):
        # Generate encryption key if it doesn't exist
        try:
            with open(self.KEY_FILE, 'rb') as key_file:
                self.key = key_file.read()
        except FileNotFoundError:
            self.generate_key()
            with open(self.KEY_FILE, 'rb') as key_file:
                self.key = key_file.read()

    def generate_key(self):
        key = Fernet.generate_key()
        with open(self.KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        print("Encryption key generated. Please store it securely.")

    def add_button(self, text, callback):
        button = Button(text=text)
        button.bind(on_press=callback)
        self.layout.add_widget(button)

    def add_product(self, instance):
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
        pass

    def update_product(self, instance):
        # Implement the update_product functionality here
        pass

    def remove_product(self, instance):
        # Implement the remove_product functionality here
        pass

    def search_product(self, instance):
        # Implement the search_product functionality here
        pass

    def sort_products(self, instance):
        # Implement the sort_products functionality here
        pass

    def filter_products(self, instance):
        # Implement the filter_products functionality here
        pass

    def view_stock(self, instance):
        # Implement the view_stock functionality here
        pass

    def generate_reports(self, instance):
        # Implement the generate_reports functionality here
        pass

if __name__ == "__main__":
    InventoryManagementApp().run()
