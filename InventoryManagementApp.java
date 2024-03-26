import java.io.*;
import java.util.*;
import java.util.stream.Collectors;

class Product {
    public int product_id;
    public String product_name;
    public int quantity;
    public double price;
    public String category;
    public String brand;
    public int sales;

    public Product(int product_id, String product_name, int quantity, double price, String category, String brand, int sales) {
        this.product_id = product_id;
        this.product_name = product_name;
        this.quantity = quantity;
        this.price = price;
        this.category = category;
        this.brand = brand;
        this.sales = sales;
    }

    public void updateSales(int quantitySold) {
        this.sales += quantitySold;
    }

    public String toCsvString() {
        return String.format("%d,%s,%d,%.2f,%s,%s,%d", product_id, product_name, quantity, price, category, brand, sales);
    }

    public static Product fromCsvString(String csvString) {
        String[] parts = csvString.split(",");
        int product_id = Integer.parseInt(parts[0]);
        String product_name = parts[1];
        int quantity = Integer.parseInt(parts[2]);
        double price = Double.parseDouble(parts[3]);
        String category = parts[4];
        String brand = parts[5];
        int sales = Integer.parseInt(parts[6]);
        return new Product(product_id, product_name, quantity, price, category, brand, sales);
    }
}

class InventoryManagementApp {
    private static final String INVENTORY_FILE = "inventory.csv";
    private static final Scanner scanner = new Scanner(System.in);
    private List<Product> inventory;

    public InventoryManagementApp() {
        this.inventory = loadInventory();
    }

    private List<Product> loadInventory() {
        try {
            BufferedReader reader = new BufferedReader(new FileReader(INVENTORY_FILE));
            List<Product> inventory = reader.lines()
                    .map(Product::fromCsvString)
                    .collect(Collectors.toList());
            reader.close();
            return inventory;
        } catch (IOException e) {
            return new ArrayList<>();
        }
    }

    private void saveInventory() {
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(INVENTORY_FILE));
            for (Product product : inventory) {
                writer.write(product.toCsvString());
                writer.newLine();
            }
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void runApplication() {
        while (true) {
            System.out.println("\nOperations:");
            System.out.println("1. Add Product");
            System.out.println("2. Update Product");
            System.out.println("3. Remove Product");
            System.out.println("4. Search Product");
            System.out.println("5. Sort Products");
            System.out.println("6. Filter Products");
            System.out.println("7. View Stock");
            System.out.println("8. Generate Reports");
            System.out.println("9. Exit");

            System.out.print("Enter your choice (1-9): ");
            String choice = scanner.nextLine();

            switch (choice) {
                case "1":
                    addProduct();
                    break;
                case "2":
                    updateProduct();
                    break;
                case "3":
                    removeProduct();
                    break;
                case "4":
                    searchProduct();
                    break;
                case "5":
                    // Implement sorting
                    break;
                case "6":
                    // Implement filtering
                    break;
                case "7":
                    // Implement viewing stock
                    break;
                case "8":
                    // Implement generating reports
                    break;
                case "9":
                    System.out.println("Exiting the program. Goodbye!");
                    saveInventory();
                    return;
                default:
                    System.out.println("Invalid choice. Please enter a number between 1 and 9.");
            }
        }
    }

    private void addProduct() {
        try {
            int productId = inventory.size() + 1;
            System.out.print("Enter product name: ");
            String productName = scanner.nextLine();
            System.out.print("Enter quantity: ");
            int quantity = Integer.parseInt(scanner.nextLine());
            System.out.print("Enter price: ");
            double price = Double.parseDouble(scanner.nextLine());
            System.out.print("Enter category: ");
            String category = scanner.nextLine();
            System.out.print("Enter brand: ");
            String brand = scanner.nextLine();

            Product newProduct = new Product(productId, productName, quantity, price, category, brand, 0);
            inventory.add(newProduct);
            System.out.println("Product added successfully!");
        } catch (NumberFormatException e) {
            System.out.println("Invalid input. Please enter a valid quantity and price.");
        }
    }

    private void updateProduct() {
        System.out.print("Enter product ID to update: ");
        int productId = Integer.parseInt(scanner.nextLine());
        for (Product product : inventory) {
            if (product.product_id == productId) {
                try {
                    System.out.print("Enter quantity sold: ");
                    int quantitySold = Integer.parseInt(scanner.nextLine());
                    product.updateSales(quantitySold);
                    product.quantity -= quantitySold;
                    System.out.println("Product updated successfully!");
                } catch (NumberFormatException e) {
                    System.out.println("Invalid input. Please enter a valid quantity.");
                }
                return;
            }
        }
        System.out.println("Product not found.");
    }

    private void removeProduct() {
        System.out.print("Enter product ID to remove: ");
        int productId = Integer.parseInt(scanner.nextLine());
        inventory.removeIf(product -> product.product_id == productId);
        System.out.println("Product removed successfully!");
    }

    private void searchProduct() {
        System.out.print("Enter keyword to search: ");
        String keyword = scanner.nextLine().toLowerCase();
        List<Product> matchingProducts = inventory.stream()
                .filter(product -> product.product_name.toLowerCase().contains(keyword))
                .collect(Collectors.toList());
        if (!matchingProducts.isEmpty()) {
            System.out.println("\nMatching Products:");
            for (Product product : matchingProducts) {
                System.out.printf("Product ID: %d, Name: %s, Quantity: %d, Price: $%.2f%n",
                        product.product_id, product.product_name, product.quantity, product.price);
            }
        } else {
            System.out.println("No matching products found.");
        }
    }

    public static void main(String[] args) {
        InventoryManagementApp app = new InventoryManagementApp();
        app.runApplication();
    }
}
