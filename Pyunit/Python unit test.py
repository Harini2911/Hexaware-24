import unittest
from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from Exception.myexceptions import ProductNotFoundException,CustomerNotFoundException


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.Order = OrderProcessorRepositoryImpl()
    # test case 1 for create a product or not

    def test_1(self):
        result=self.Order.create_product_test("Aristocrat bags",2000.00,"it is a luggage bag",1000)
        self.assertEqual(True,result)
        result = self.Order.create_product_test("Aristocrat bags", "good", "It is a premium watch", 2000)
        self.assertEqual(False, result)
    # test case 2 for adding items in to cart

    def test_2(self):
        result=self.Order.add_to_cart(1,19,4)
        self.assertEqual(True,result)
        result = self.Order.add_to_cart(-4, 21, 4)
        self.assertEqual(False, result)
    # test case 3 for placing order or not

    def test_3(self):
        result=self.Order.place_order(4,{4:2},"Nellore")
        self.assertEqual(True,result)
    # test case 4 for ProductNotFoundException

    def test_4(self):
        with self.assertRaises(ProductNotFoundException):
            self.Order.delete_product(25)
    # test case 5 for CustomerNotFoundException

    def test_5(self):
        with self.assertRaises(CustomerNotFoundException):
            self.Order.delete_customer(4)


if __name__ == '__main__':
    unittest.main()
