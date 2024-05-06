from abc import ABC, abstractmethod


class OrderProcessorRepository(ABC):
    @abstractmethod
    def create_product(self, products):
        pass

    @abstractmethod
    def create_customer(self, customers):
        pass

    @abstractmethod
    def delete_product(self, product_id):
        pass

    @abstractmethod
    def delete_customer(self, customer_id):
        pass

    @abstractmethod
    def add_to_cart(self, customers, products, quantity):
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
    def get_orders_by_customer(self, customer_id):
        pass

    @abstractmethod
    def get_product(self, product_id):
        pass

