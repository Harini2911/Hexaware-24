from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from Entity.Customers import Customers
from Entity.Products import Products
from Exception.myexceptions import CustomerNotFoundException, ProductNotFoundException, OrderNotFoundException,InsufficientStockException,InvalidDataException
from util.dbConnection import DBConnection
from dao.OrderProcessorRepositoryImpl import *


class MainModule:
    def __init__(self):
        self.order_processor = OrderProcessorRepositoryImpl()

    @staticmethod
    def display_menu():
        print("Welcome to the Ecommerce Application")
        print("1. Register Customer")
        print("2. Update Customer")
        print("3. View Customers")
        print("4. To retrieve a specific Customer")
        print("5. Delete Customer")
        print("6. Create Product")
        print("7. Update Products")
        print("8. View Products")
        print("9. Delete Product")
        print("10. To retrieve a specific Product")
        print("11. Add to Cart")
        print("12. View Cart")
        print("13. Remove from cart")
        print("14. Place Order")
        print("15. Update Order")
        print("16. Cancel Order")
        print("17. View Customer Order")
        print("18. create order items")
        print("19. Update order items")
        print("20. View order items")
        print("21. Delete order items")
        print("22. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                self.create_customer()
            elif choice == '2':
                self.update_customer()
            elif choice == '3':
                self.view_customers()
            elif choice == '4':
                self.retrieve_customer()
            elif choice == '5':
                self.delete_customer()
            elif choice == '6':
                self.create_product()
            elif choice == '7':
                self.update_product()
            elif choice == '8':
                self.view_products()
            elif choice == '9':
                self.delete_product()
            elif choice == '10':
                self.retrieve_product()
            elif choice == '11':
                self.add_to_cart()
            elif choice == '12':
                self.view_cart()
            elif choice == '13':
                self.remove_from_cart()
            elif choice == '14':
                self.place_order()
            elif choice == '15':
                self.update_order()
            elif choice == '16':
                self.cancel_order()
            elif choice == '17':
                self.view_customer_order()
            elif choice == '18':
                self.create_order_items()
            elif choice == '19':
                self.update_order_items()
            elif choice == '20':
                self.view_order_items()
            elif choice == '21':
                self.delete_order_items()
            elif choice == '22':
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

    def update_customer(self):
        customer_id = int(input("Enter customer_id to update :"))
        new_name = input("Enter new name to update :")
        new_email = input("Enter new email to update :")
        success = self.order_processor.update_customer(customer_id, new_name, new_email)
        if success:
            print("customer updated successfully.")
        else:
            print("Failed to update customer.")

    def view_customers(self):
        success = self.order_processor.view_customers(Customers)
        if success:
            print("all customers viewed successfully.")
        else:
            print("Failed to view customers.")

    def retrieve_customer(self):
        customer_id = int(input("Enter customer_id to retrieve customer :"))
        success = self.order_processor.retrieve_customer(customer_id)
        if success:
            print("customer retrieved successfully.")
        else:
            print("Failed to retrieved customer.")

    def delete_customer(self):
        customer_id = int(input("Enter customer_id to delete particular customer :"))
        success = self.order_processor.delete_customer(customer_id)
        if success:
            print("customer deleted successfully.")
        else:
            print("Failed to delete customer.")

    def retrieve_product(self):
        product_id = int(input("Enter product_id to retrieve particular product :"))
        success = self.order_processor.get_product(product_id)
        if success:
            print("product retrieved successfully.")
        else:
            print("Failed to retrieve product.")

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

    def update_product(self):
        product_id = int(input("Enter product ID to update: "))
        new_name = input("Enter new name to update:")
        new_price = float(input("Enter new price to update:"))
        new_description = input("Enter new description to update:")
        new_stock_quantity = int(input("Enter new stock quantity to update:"))
        success = self.order_processor.update_product(new_name, new_price, new_description, new_stock_quantity,
                                                      product_id)
        if success:
            print("Product updated successfully.")
        else:
            print("Failed to update product.")

    def view_products(self):
        success = self.order_processor.view_products(Products)
        if success:
            print("Products viewed successfully.")
        else:
            print("Failed to viewed products.")

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
        success = self.order_processor.add_to_cart(customer_id, product_id, quantity)

        if success:
            print("Product added to cart successfully.")
        else:
            print("Failed to add product to cart.")

    def remove_from_cart(self):
        customer_id = int(input("Enter customer ID: "))
        product_id = int(input("Enter product ID to remove to cart: "))
        success = self.order_processor.remove_from_cart(customer_id, product_id)
        if success:
            print("Product removed from cart successfully.")
        else:
            print("Failed to removed product from cart.")

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
        customer_id = int(input("Enter customer ID to place order: "))
        shipping_address = input("Enter shipping address: ")
        products_quantity_map = self.order_processor.get_all_from_cart(customer_id)
        print("Products quantity map:", products_quantity_map)  # Add this line for debugging
        success = self.order_processor.place_order(customer_id, products_quantity_map, shipping_address)
        if success:
            print("Order placed successfully.")
        else:
            print("Failed to place order.")

    def update_order(self):
        order_id = int(input("Enter order ID to update:"))
        new_order_date = input("Enter the new order date (YYYY-MM-DD): ")
        new_shipping_address = input("Enter the new shipping address: ")
        success = self.order_processor.update_order(order_id, new_order_date, new_shipping_address)
        if success:
            print("Update Order successfully.")
        else:
            print("Failed to update order.")

    def cancel_order(self):
        order_id = int(input("Enter order ID to cancel: "))
        success = self.order_processor.cancel_order(order_id)
        if success:
            print("Order cancelled successfully.")
        else:
            print("Failed to cancel order.")

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

    def create_order_items(self):
        order_id = int(input("Enter order Id :"))
        product_id = int(input("Enter product_id :"))
        quantity = int(input("Enter quantity :"))
        success = self.order_processor.create_order_items(order_id, product_id, quantity)
        if success:
            print("Order items created successfully.")
        else:
            print("Failed to create order items.")

    def update_order_items(self):
        new_quantity = int(input("Enter new quantity :"))
        order_item_id = int(input("Enter order item id :"))
        success = self.order_processor.update_order_items(new_quantity, order_item_id)
        if success:
            print("Order items updated successfully.")
        else:
            print("Failed to update order items.")

    def view_order_items(self):
        order_id = int(input("Enter order ID :"))
        success = self.order_processor.view_order_items(order_id)
        if success:
            print("Order items viewed successfully.")
        else:
            print("Failed to viewed order items.")

    def delete_order_items(self):
        order_item_id = int(input("Enter order item id :"))
        success = self.order_processor.delete_order_items(order_item_id)
        if success:
            print("Order items deleted successfully.")
        else:
            print("Failed to deleted order items.")

    def get_all_from_cart(self, customer_id):
        pass


if __name__ == "__main__":
    app = MainModule()
    app.run()


