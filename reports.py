from product_operations import load_inventory

def sales_report():
    inventory = load_inventory()
    
    print("\nSales Report:")
    for product in inventory:
        total_quantity_sold = product.sales
        total_revenue = total_quantity_sold * product.price
        
        print(f"Product: {product.product_name}, Total Quantity Sold: {total_quantity_sold}, Total Revenue: ${total_revenue:.2f}")

def inventory_turnover_report():
    inventory = load_inventory()
    
    print("\nInventory Turnover Report:")
    for product in inventory:
        turnover_rate = product.sales / product.quantity if product.quantity != 0 else 0
        print(f"Product: {product.product_name}, Turnover Rate: {turnover_rate:.2f} times per unit")

def financial_report():
    inventory = load_inventory()

    total_revenue = sum(product.sales * product.price for product in inventory)
    total_cogs = sum(product.quantity * product.price for product in inventory)
    total_profit = total_revenue - total_cogs
    
    print("\nFinancial Report:")
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Total Cost of Goods Sold (COGS): ${total_cogs:.2f}")
    print(f"Total Profit: ${total_profit:.2f}")

def top_products_report(sort_by='sales', num_top=5):
    inventory = load_inventory()
    
    sorted_inventory = sorted(inventory, key=lambda x: getattr(x, sort_by), reverse=True)[:num_top]
    
    print(f"\nTop Products Report (Sorted by {sort_by}):")
    for product in sorted_inventory:
        print(f"Product: {product.product_name}, {sort_by.capitalize()}: ${getattr(product, sort_by):.2f}")

def low_stock_report(threshold=10):
    inventory = load_inventory()
    
    low_stock_products = [product for product in inventory if product.quantity < threshold]
    
    if not low_stock_products:
        print("\nNo products below the specified stock threshold.")
        return

    print(f"\nLow Stock Report (Threshold: {threshold}):")
    for product in low_stock_products:
        print(f"Product: {product.product_name}, Current Stock: {product.quantity}")
