from abc import ABC, abstractmethod


class OrderProcessorRepository(ABC):
    @abstractmethod
    def create_product(self, products):
        pass

    @abstractmethod
    def create_customer(self, customers):
        pass

    @abstractmethod
    def update_customer(self, customer_id,new_name,new_email):
        pass

    @abstractmethod
    def view_customers(self,customers):
        pass

    @abstractmethod
    def retrieve_customer(self,customer_id):
        pass

    @abstractmethod
    def view_products(self,products):
        pass

    @abstractmethod
    def delete_product(self, product_id):
        pass

    @abstractmethod
    def update_product(self,new_name, new_price, new_description, new_stock_quantity, product_id):
        pass

    @abstractmethod
    def delete_customer(self, customer_id):
        pass

    @abstractmethod
    def add_to_cart(self, customer_id, product_id, quantity):
        pass

    @abstractmethod
    def remove_from_cart(self, customers, products):
        pass

    @abstractmethod
    def get_all_from_cart(self, customers):
        pass

    @abstractmethod
    def place_order(self, customers, products_quantity_map, shipping_address):
        pass

    @abstractmethod
    def cancel_order(self,order_id):
        pass

    def update_order(self,order_id, new_order_date,new_shipping_address):
        pass

    @abstractmethod
    def get_orders_by_customer(self, customer_id):
        pass

    @abstractmethod
    def get_product(self, product_id):
        pass

    @abstractmethod
    def create_order_items(self,order_id, product_id, quantity):
        pass

    @abstractmethod
    def update_order_items(self,new_quantity,order_item_id):
        pass

    @abstractmethod
    def view_order_items(self,order_id):
        pass

    @abstractmethod
    def delete_order_items(self,order_item_id):
        pass


