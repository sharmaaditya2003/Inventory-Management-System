from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from cryptography.fernet import Fernet
import json

class InventoryManagementApp(GridLayout):
    def __init__(self, **kwargs):
        super(InventoryManagementApp, self).__init__(**kwargs)
        self.cols = 1

        self.KEY_FILE = 'encryption_key.key'
        self.key = self.get_key()

        self.create_widgets()

    def create_widgets(self):
        self.label = Label(text="Inventory Management System", font_size=20)
        self.add_widget(self.label)

        self.key_input = TextInput(hint_text="Enter your encryption key", multiline=False, password=True)
        self.add_widget(self.key_input)

        self.login_button = Button(text="Login")
        self.login_button.bind(on_press=self.login)
        self.add_widget(self.login_button)

    def login(self, instance):
        user_key = self.key_input.text

        if self.key is None:
            self.show_popup("Key Error", "No encryption key found. Please generate a key.")
            return

        if user_key != self.key.decode('utf-8'):
            self.show_popup("Login Failed", "Incorrect encryption key. Please try again.")
            return

        self.clear_widgets()
        self.main_menu()

    def main_menu(self):
        self.label.text = "Main Menu"

        operations = ["Add Product", "Update Product", "Remove Product", "Search Product", "Sort Products", "Filter Products", "View Stock", "Generate Reports", "Exit"]

        for operation in operations:
            button = Button(text=operation)
            button.bind(on_press=self.handle_operation)
            self.add_widget(button)

    def handle_operation(self, instance):
        self.show_popup("Operation Selected", f"You selected: {instance.text}")

    def show_popup(self, title, message):
        content = Label(text=message)
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

    def get_key(self):
        try:
            with open(self.KEY_FILE, 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            return None

class InventoryManagementAppApp(App):
    def build(self):
        return InventoryManagementApp()

if __name__ == "__main__":
    InventoryManagementAppApp().run()
