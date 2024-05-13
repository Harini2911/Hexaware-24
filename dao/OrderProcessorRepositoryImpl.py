import mysql.connector
from mysql.connector import Error
from dao.OrderProcessorRepository import OrderProcessorRepository
from Exception.myexceptions import InsufficientStockException, OrderNotFoundException, CustomerNotFoundException, ProductNotFoundException
from util.dbConnection import DBConnection
from Entity.Customers import Customers
from Entity.Products import Products


class OrderProcessorRepositoryImpl(DBConnection,OrderProcessorRepository):
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Harini2002",
            database="ECOM"
        )

    def create_product(self,products):
        try:
            stmt = self.conn.cursor()
            query = "INSERT INTO products (name, price, description, stockQuantity) VALUES (%s, %s, %s, %s)"
            stmt.execute(query,(products.get_name(),products.get_price(),products.get_description(),products.get_stock_quantity()))
            self.conn.commit()
            return True
        except Error as e:
            print("Error while inserting product:",e)
            return False

    def create_product_test(self,name,price,description,stock_quantity):
        try:
            stmt = self.conn.cursor()
            query = "INSERT INTO products (name, price, description, stockQuantity) VALUES (%s, %s, %s, %s)"
            stmt.execute(query,(name,price,description,stock_quantity))
            self.conn.commit()
            return True
        except Error as e:
            print("Error while inserting product:",e)
            return False

    def create_customer(self,customers):
        try:
            stmt= self.conn.cursor()
            query = "INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)"
            stmt.execute(query, (customers.get_name(),customers.get_email(),customers.get_password()))
            self.conn.commit()
            return True
        except Error as e:
            print("Error while inserting customer:", e)
            return False

    def update_customer(self,customer_id,new_name,new_email):
        try:
            stmt=self.conn.cursor()
            query="UPDATE customers SET name = %s, email = %s WHERE customer_id = %s"
            stmt.execute(query,(new_name, new_email, customer_id))
            self.conn.commit()
            print("Customer info updated successfully")
            return True
        except Error as e:
            print("Error while updating customer:", e)

    def view_customers(self,customers):
        try:
            stmt=self.conn.cursor()
            query="select * from Customers"
            stmt.execute(query)
            customer_data = stmt.fetchall()
            if customer_data:
                print("List of Customers:")
                for customer in customer_data:
                    print("Customer ID:", customer[0])
                    print("Name:", customer[1])
                    print("Email:", customer[2])
                    print("-------------------")
                return True
            else:
                print("No customers found in the database.")
                return False
        except mysql.connector.Error as error:
            print("Error retrieving customers:", error)
            return False

    def retrieve_customer(self,customer_id):
        try:
            stmt=self.conn.cursor()
            query="select * from Customers where customer_id = %s"
            stmt.execute(query,(customer_id,))
            result=stmt.fetchone()
            if result:
                print("Customer ID:", result[0])
                print("Name:", result[1])
                print("Email:", result[2])
                return True
            else:
                print("No customer found with ID:", customer_id)
                return False
        except Error as e:
            print("Failed in retrieve customer:",e)
            return False

    def update_product(self,new_name, new_price, new_description, new_stock_quantity, product_id):
        try:
            stmt = self.conn.cursor()
            query = """
    UPDATE products 
    SET name = %s, price = %s, description = %s, stockQuantity = %s 
    WHERE product_id = %s
"""
            stmt.execute(query,(new_name, new_price, new_description, new_stock_quantity, product_id))
            self.conn.commit()
            return True

        except Error as e:
            print("Failed to update products:",e)
            return False

    def view_products(self,products):
        try:
            stmt=self.conn.cursor()
            query="select * from Products"
            stmt.execute(query)
            product_data = stmt.fetchall()
            if product_data:
                print("List of Customers:")
                for product in product_data:
                    print("Product ID:", product[0])
                    print("Name:", product[1])
                    print("price:", product[2])
                    print("Description:",product[3])
                    print("StockQuantity:",product[4])
                    print("-------------------")
                return True
            else:
                print("No products found in the database.")
        except Error as e:
            print("Failed to view products:",e)

    def delete_product(self, product_id):
        try:
            stmt = self.conn.cursor()
            query = "SELECT COUNT(*) FROM products WHERE product_id = %s"
            stmt.execute(query, (product_id,))
            result = stmt.fetchone()
            if result[0] == 0:
                raise ProductNotFoundException("Product ID not found in the database")
            else:
                stmt.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
                self.conn.commit()
                return True
        except Error as e:
            print("Error while deleting product:", e)
            return False

    def delete_customer(self, customer_id):
        try:
            stmt = self.conn.cursor()
            query = "SELECT COUNT(*) FROM customers WHERE customer_id = %s"
            stmt.execute(query, (customer_id,))
            result = stmt.fetchone()
            if result[0] == 0:
                raise CustomerNotFoundException("Customer ID not found in the database")
            else:
                stmt.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
                self.conn.commit()
                return True
        except Error as e:
            print("Error while deleting customer:", e)
            return False

    def add_to_cart(self,customer_id, product_id, quantity):
        stmt = self.conn.cursor()
        if int(customer_id)<0:
            return False
        query = "INSERT INTO cart (customer_id, product_id, quantity) VALUES (%s,%s, %s)"
        stmt.execute(query,(customer_id, product_id, quantity))
        self.conn.commit()
        if stmt.rowcount>0:
            print("product added")
            return True
        else:
            print("Failed to add product to cart.")
            return False

    def remove_from_cart(self, customer_id,product_id):
        try:
            stmt = self.conn.cursor()
            query = "DELETE FROM cart WHERE customer_id = %s AND product_id = %s"

            stmt.execute(query, (customer_id,product_id))
            self.conn.commit()
            return True
        except Error as e:
            print("Error while removing from cart:", e)
            return False

    def get_all_from_cart(self, customer_id):
        try:
            stmt = self.conn.cursor()
            query = "SELECT product_id, SUM(quantity) FROM cart WHERE customer_id = %s GROUP BY product_id"
            stmt.execute(query, (customer_id,))
            rows = stmt.fetchall()
            products_quantity_map = [{'product_id': row[0], 'quantity': row[1]} for row in rows]
            return products_quantity_map
        except Error as e:
            print("Error while getting from cart:", e)
            return False

    def place_order(self, customer_id, products_quantity_map, shipping_address):
        try:
            total_price=0
            for product_quantity in products_quantity_map:
                #product_id=product_quantity["product_id"]
                product_id=product_quantity
                #quantity=product_quantity["quantity"]
                quantity=products_quantity_map[product_quantity]
                print(product_id, quantity)
                product=self.get_product(product_id)
                print(product)
                if quantity > product.get_stock_quantity():
                    raise InsufficientStockException(f"Insufficient stock for product with ID {product_id}.")
                total_price=total_price+(product.get_price()*quantity)
            print(total_price)
            stmt=self.conn.cursor()
            query="insert into orders(customer_id,order_date,total_price,shipping_address) values (%s,Now(),%s,%s)"
            stmt.execute(query, (customer_id,total_price,shipping_address))
            self.conn.commit()
            order_id=stmt.lastrowid
            query="insert into order_items(order_id, product_id, quantity) values (%s,%s,%s)"
            for product_quantity in products_quantity_map:
                product_id = product_quantity
                quantity = products_quantity_map[product_quantity]
                #product_id=product_quantity["product_id"]
                #quantity=product_quantity["quantity"]
                stmt.execute(query,(order_id,product_id,quantity))
            self.conn.commit()
            return True
        except Error as e:
            print("Error while placing order:",e)
            return False

    def update_order(self, order_id, new_order_date,new_shipping_address):
        try:
            stmt = self.conn.cursor()
            query= "UPDATE orders SET order_date = %s,shipping_address = %s WHERE order_id = %s"
            stmt.execute(query,(new_order_date,new_shipping_address, order_id))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error updating order:", e)
            return False

    def cancel_order(self,order_id):
        try:
            stmt = self.conn.cursor()
            query = "SELECT * FROM orders WHERE order_id = %s"
            stmt.execute(query, (order_id,))
            order = stmt.fetchone()
            if not order:
                print("Order not found.")
                return False
            query = "DELETE FROM orders WHERE order_id = %s"
            stmt.execute(query, (order_id,))

            query = "DELETE FROM order_items WHERE order_id = %s"
            stmt.execute(query, (order_id,))
            self.conn.commit()
            return True
        except Error as e:
            print("Error while canceling order:", e)
            return False

    def get_product(self, product_id):
        try:
            stmt = self.conn.cursor()
            query = "SELECT * FROM Products WHERE product_id = %s"
            stmt.execute(query,(product_id,))
            product_values = stmt.fetchall()
            if product_values:
                print(product_values)
                return Products(*product_values[0])
            else:
                print("No product found with ID:", product_id)
                return None
        except Exception as e:
            print("Error while getting product:", e)
            return False

    def get_orders_by_customer(self, customer_id):
        try:
            stmt = self.conn.cursor()
            query = """
                SELECT orders.order_id, orders.order_date, orders.total_price, orders.shipping_address, 
                order_items.product_id, order_items.quantity, products.name 
                FROM orders 
                JOIN order_items ON orders.order_id = order_items.order_id 
                JOIN products ON order_items.product_id = products.product_id 
                WHERE orders.customer_id = %s
            """
            stmt.execute(query, (customer_id,))
            rows = stmt.fetchall()
            if not rows:
                raise OrderNotFoundException(f"No orders found for customer with ID {customer_id}.")
            orders = {}
            for row in rows:
                order_id = row[0]
                if order_id not in orders:
                    orders[order_id] = {'order_id': order_id,'order_date': row[1],'total_price': row[2],'shipping_address': row[3],'items': []}
                orders[order_id]['items'].append({'product_id': row[4],'quantity': row[5],'product_name': row[6]})
            return list(orders.values())
        except OrderNotFoundException as e:
            print(f'Order not found{customer_id}')
        except Error as e:
            print("Error while fetching orders:", e)
            return []

    def get_stock_quantity(self, product_id):
        try:
            stmt=self.conn.cursor()
            query = "SELECT stock_quantity FROM products WHERE product_id = %s"
            stmt.execute(query, (product_id,))
            result = stmt.fetchone()
            stmt.close()
            if result:
                return result[0]  # Return the stock quantity
            else:
                return None  # Product not found

        except Exception as e:
            print("Error while retrieving stock quantity:", e)
            return None

    def create_order_items(self, order_id, product_id, quantity):
        try:
            stmt = self.conn.cursor()
            query = "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)"
            stmt.execute(query, (order_id, product_id, quantity))
            self.conn.commit()
            return True
        except Error as e:
            print("Error creating order item:", e)
            return False

    def update_order_items(self, new_quantity,order_item_id):
        try:
            stmt = self.conn.cursor()
            query = "UPDATE order_items SET quantity = %s WHERE order_item_id = %s"
            stmt.execute(query, (new_quantity,order_item_id))
            self.conn.commit()
            return True
        except Error as e:
            print("Error updating order item:", e)
            return False

    def view_order_items(self, order_id):
        try:
            stmt = self.conn.cursor()
            query = "SELECT * FROM order_items WHERE order_id = %s"
            stmt.execute(query, (order_id,))
            order_items = stmt.fetchall()
            if order_items:
                print("Order items:")
                for item in order_items:
                    print(f"Order Item ID: {item[0]}")
                    print(f"Order ID: {item[1]}")
                    print(f"Product ID: {item[2]}")
                    print(f"Quantity: {item[3]}")
                    print()
            else:
                print("No order items found for the specified order ID.")
        except Error as e:
            print("Error retrieving order items:", e)

    def delete_order_items(self,order_item_id):
        try:
            stmt = self.conn.cursor()
            query = "DELETE FROM order_items WHERE order_item_id = %s"
            stmt.execute(query, (order_item_id,))
            self.conn.commit()
            return True
        except Error as e:
            print("Error deleting order item:", e)
            return False

    def __del__(self):
        if self.conn.is_connected():
            self.conn.close()
