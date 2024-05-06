from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from Entity.Customers import Customers
from Entity.Products import Products
from Exception.myexceptions import CustomerNotFoundException, ProductNotFoundException, OrderNotFoundException,InsufficientStockException
from util.dbConnection import DBConnection
from dao.OrderProcessorRepositoryImpl import *

class MainModule:
    def __init__(self):
        self.order_processor = OrderProcessorRepositoryImpl()

    def display_menu(self):
        print("Welcome to the Ecommerce Application")
        print("1. Create Customer")
        print("2. Create Product")
        print("3. Delete Product")
        print("4. Add to Cart")
        print("5. View Cart")
        print("6. Place Order")
        print("7. View Customer Order")
        print("8. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                self.create_customer()
            elif choice == '2':
                self.create_product()
            elif choice == '3':
                self.delete_product()
            elif choice == '4':
                self.add_to_cart()
            elif choice == '5':
                self.view_cart()
            elif choice == '6':
                self.place_order()
            elif choice == '7':
                self.view_customer_order()
            elif choice == '8':
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please try again.")

    def create_customer(self):
        name = input("Enter customer name: ")
        email = input("Enter customer email: ")
        password = input("Enter customer password: ")
        customer = Customers(name=name, email=email, password=password)  # Creating a Customers object
        success = self.order_processor.create_customer(customer)
        if success:
            print("Customer registered successfully.")
        else:
            print("Failed to register customer.")

    def create_product(self):
        name = input("Enter product name: ")
        price = float(input("Enter product price: "))
        description = input("Enter product description: ")
        stock_quantity = int(input("Enter product stock quantity: "))
        product = Products(name=name, price=price, description=description, stock_quantity=stock_quantity)
        success = self.order_processor.create_product(product)
        if success:
            print("Product created successfully.")
        else:
            print("Failed to create product.")

    def delete_product(self):
        product_id = int(input("Enter product ID to delete: "))
        success = self.order_processor.delete_product(product_id)
        if success:
            print("Product deleted successfully.")
        else:
            print("Failed to delete product.")

    def add_to_cart(self):
        customer_id = int(input("Enter customer ID: "))
        product_id = int(input("Enter product ID to add to cart: "))
        quantity = int(input("Enter quantity to add to cart: "))
        success = self.order_processor.add_to_cart(customer_id,product_id, quantity)

        if success:
            print("Product added to cart successfully.")
        else:
            print("Failed to add product to cart.")

    def view_cart(self):
        customer_id = int(input("Enter customer ID to view cart: "))
        cart_items = self.order_processor.get_all_from_cart(customer_id)
        if cart_items:
            print("Products in cart:")
            for item in cart_items:
                print(f"Product ID: {item['product_id']}, Quantity: {item['quantity']}")
        else:
            print("Cart is empty.")
    def place_order(self):
        customer_id=int(input("Enter customer ID to place order: "))
        shipping_address = input("Enter shipping address: ")
        products_quantity_map = self.order_processor.get_all_from_cart(customer_id)
        print(products_quantity_map)
        success = self.order_processor.place_order(customer_id,products_quantity_map, shipping_address)
        if success:
            print("Order placed successfully.")
        else:
            print("Failed to place order.")




    def view_customer_order(self):
        customer_id = int(input("Enter customer ID: "))
        orders = self.order_processor.get_orders_by_customer(customer_id)
        if orders:
            print("Customer Orders:")
            for order in orders:
                print(
                    f"Order ID: {order['order_id']}, Order Date: {order['order_date']}, Total Price: {order['total_price']}, Shipping Address: {order['shipping_address']}")
        else:
            print("No orders found for the customer.")

    def get_all_from_cart(self,customer_id):
        pass





if __name__ == "__main__":
    app = MainModule()
    app.run()
