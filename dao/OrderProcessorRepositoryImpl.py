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

    def create_product(self, products):
        try:
            stmt = self.conn.cursor()
            query = "INSERT INTO products (name, price, description, stockQuantity) VALUES (%s, %s, %s, %s)"
            stmt.execute(query,(products.get_name(), products.get_price(), products.get_description(), products.get_stock_quantity()))
            self.conn.commit()
            return True
        except Error as e:
            print("Error while inserting product:",e)
            return False

    def create_customer(self, customers):
        try:
            stmt= self.conn.cursor()
            query = "INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)"
            stmt.execute(query, (customers.get_name(), customers.get_email(), customers.get_password()))
            self.conn.commit()
            return True
        except Error as e:
            print("Error while inserting customer:", e)
            return False

    def delete_product(self, product_id):
        try:
            stmt = self.conn.cursor()
            query = "SELECT COUNT(*) FROM products WHERE product_id = %s"
            stmt.execute(query, (product_id,))
            result = stmt.fetchone()
            if result[0] > 0:
                try:
                    stmt = self.conn.cursor()
                    query = "DELETE FROM products WHERE product_id = %s"
                    stmt.execute(query, (product_id,))
                    self.conn.commit()
                    return True
                except Error as e:
                    print("Error while deleting product:", e)
                    return False
            else:
                raise ProductNotFoundException("Product id not found in the database")
        except ProductNotFoundException as e:
            print(f'deletion failed {e}')

    def delete_customer(self, customer_id):
        try:
            stmt = self.conn.cursor()
            query = "SELECT COUNT(*) FROM customers WHERE id = %s"
            stmt.execute(query, (customer_id,))
            result = stmt.fetchone()
            if result[0]>0:
                try:
                    stmt = self.conn.cursor()
                    query = "DELETE FROM customers WHERE customer_id = %s"
                    stmt.execute(query, customer_id)
                    self.conn.commit()
                    return True
                except Error as e:
                    print("Error while deleting customer:", e)
                    return False
            else:
                raise CustomerNotFoundException("customer id not found in the database")
        except CustomerNotFoundException as e:
            print(f'deletion failed {e}')

    def add_to_cart(self,customer_id, product_id, quantity):
        stmt = self.conn.cursor()
        query = "INSERT INTO cart (customer_id, product_id, quantity) VALUES (%s,%s, %s)"
        stmt.execute(query,(customer_id, product_id, quantity))
        self.conn.commit()
        if stmt.rowcount>0:
            print("product added")
            return True
        else:
            print("Failed to add product to cart.")
            return False

    def remove_from_cart(self, customers,products):
        try:
            stmt = self.conn.cursor()
            query = "DELETE FROM cart WHERE customer_id = %s AND product_id = %s"
            stmt.execute(query, (Customers.get_customer_id(), Products.get_product_id()))
            self.conn.commit()
            return True
        except Error as e:
            print("Error while removing from cart:", e)
            return False

    def get_all_from_cart(self,customer_id):
        try:
            stmt=self.conn.cursor()
            query="select product_id,quantity from cart where customer_id= %s"
            stmt.execute(query,(customer_id,))
            rows=stmt.fetchall()
            products_quantity_map = [{'product_id': row[0], 'quantity': row[1]} for row in rows]
            return products_quantity_map
            self.conn.commit()
            return rows
        except Error as e:
            print("Error while getting from cart:",e)
            return False

    def place_order(self, customer_id, products_quantity_map, shipping_address):
        try:
            total_price=0
            for product_quantity in products_quantity_map:
                product_id=product_quantity["product_id"]
                quantity=product_quantity["quantity"]
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
            order_id=stmt.lastrowid
            query="insert into order_items(order_id, product_id, quantity) values (%s,%s,%s)"
            for product_quantity in products_quantity_map:
                product_id=product_quantity["product_id"]
                quantity=product_quantity["quantity"]
                stmt.execute(query,(order_id,product_id,quantity))
            self.conn.commit()
            return True
        except Error as e:
            print("Error while placing order:",e)
            return False

    def get_product(self, product_id):
        try:
            # Create a cursor object using the existing connection
            stmt = self.conn.cursor()

            # SQL query with placeholder for parameters
            query = "SELECT * FROM Products WHERE product_id = %s"

            # Execute the query with the parameter tuple
            stmt.execute(query,(product_id,))

            # Fetch all the results
            product_values = stmt.fetchall()

            # Check if product_values has any rows
            if product_values:
                print(product_values)
                # Assuming your Products class is initialized with a row of data like this:
                # Ensure the number of fields matches the constructor of the Products class
                return Products(*product_values[0])  # Unpack the first row directly if only one is expected
            else:
                print("No product found with ID:", product_id)
                return None
        except Exception as e:  # Catch a more general exception to ensure all errors are caught
            print("Error while getting product:", e)
            return False
        finally:
            stmt.close()

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

    def __del__(self):
        if self.conn.is_connected():
            self.conn.close()
