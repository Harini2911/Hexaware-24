class CustomerNotFoundException(Exception):
    def __init__(self,msg="Customer not found in the database"):
        self.msg = msg
        super().__init__(self.msg)


class ProductNotFoundException(Exception):
    def __init__(self,msg="Product not found in the database"):
        self.msg = msg
        super().__init__(self.msg)


class OrderNotFoundException(Exception):
    def __init__(self,msg="Order not found in the database"):
        self.msg = msg
        super().__init__(self.msg)


class InsufficientStockException(Exception):
    def __init__(self,msg="insufficient stock quantity"):
        self.msg = msg
        super().__init__(self.msg)
