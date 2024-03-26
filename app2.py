from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
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

class InventoryManagementApp(App):
    def __init__(self, **kwargs):
        super(InventoryManagementApp, self).__init__(**kwargs)
        self.inventory = []
        self.load_inventory()

    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.add_product_layout = GridLayout(cols=2)
        self.add_product_layout.add_widget(Label(text='Product Name:'))
        self.product_name_input = TextInput()
        self.add_product_layout.add_widget(self.product_name_input)

        self.add_product_layout.add_widget(Label(text='Quantity:'))
        self.quantity_input = TextInput()
        self.add_product_layout.add_widget(self.quantity_input)

        self.add_product_layout.add_widget(Label(text='Price:'))
        self.price_input = TextInput()
        self.add_product_layout.add_widget(self.price_input)

        self.add_product_layout.add_widget(Label(text='Category:'))
        self.category_input = TextInput()
        self.add_product_layout.add_widget(self.category_input)

        self.add_product_layout.add_widget(Label(text='Brand:'))
        self.brand_input = TextInput()
        self.add_product_layout.add_widget(self.brand_input)

        self.add_product_layout.add_widget(Label())
        self.add_product_button = Button(text='Add Product', on_press=self.add_product)
        self.add_product_layout.add_widget(self.add_product_button)

        self.layout.add_widget(self.add_product_layout)

        self.product_list_layout = ScrollView()
        self.product_list_grid = GridLayout(cols=7, size_hint_y=None)
        self.product_list_grid.bind(minimum_height=self.product_list_grid.setter('height'))
        self.product_list_layout.add_widget(self.product_list_grid)
        self.update_product_list()

        self.layout.add_widget(self.product_list_layout)

        return self.layout

    def add_product(self, instance=None):
        try:
            product_id = len(self.inventory) + 1
            product_name = self.product_name_input.text
            quantity = int(self.quantity_input.text)
            price = float(self.price_input.text)
            category = self.category_input.text
            brand = self.brand_input.text
            new_product = Product(product_id, product_name, quantity, price, category, brand)
            self.inventory.append(new_product)
            self.update_product_list()
        except ValueError:
            self.show_message('Error', 'Invalid input. Please enter a valid quantity and price.')

    def update_product_list(self):
        self.product_list_grid.clear_widgets()
        self.product_list_grid.add_widget(Label(text='Product ID'))
        self.product_list_grid.add_widget(Label(text='Product Name'))
        self.product_list_grid.add_widget(Label(text='Quantity'))
        self.product_list_grid.add_widget(Label(text='Price'))
        self.product_list_grid.add_widget(Label(text='Category'))
        self.product_list_grid.add_widget(Label(text='Brand'))
        self.product_list_grid.add_widget(Label(text='Sales'))
        for product in self.inventory:
            self.product_list_grid.add_widget(Label(text=str(product.product_id)))
            self.product_list_grid.add_widget(Label(text=product.product_name))
            self.product_list_grid.add_widget(Label(text=str(product.quantity)))
            self.product_list_grid.add_widget(Label(text=str(product.price)))
            self.product_list_grid.add_widget(Label(text=product.category))
            self.product_list_grid.add_widget(Label(text=product.brand))
            self.product_list_grid.add_widget(Label(text=str(product.sales)))

    def load_inventory(self):
        try:
            with open('inventory.json', 'r') as file:
                inventory_data = json.load(file)
                for product_data in inventory_data:
                    product = Product(**product_data)
                    self.inventory.append(product)
        except FileNotFoundError:
            pass

    def save_inventory(self):
        inventory_data = []
        for product in self.inventory:
            inventory_data.append({
                'product_id': product.product_id,
                'product_name': product.product_name,
                'quantity': product.quantity,
                'price': product.price,
                'category': product.category,
                'brand': product.brand,
                'sales': product.sales
            })
        with open('inventory.json', 'w') as file:
            json.dump(inventory_data, file, indent=4)

    def on_stop(self):
        self.save_inventory()

    def show_message(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        ok_button = Button(text='OK')
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(300, 200), auto_dismiss=False)
        ok_button.bind(on_press=popup.dismiss)
        content.add_widget(ok_button)
        popup.open()

if __name__ == '__main__':
    InventoryManagementApp().run()
