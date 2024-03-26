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
