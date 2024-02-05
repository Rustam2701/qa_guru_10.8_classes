import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:

    def test_product_check_quantity(self, product):
        assert product.check_quantity(500)
        assert not product.check_quantity(1500)

    def test_product_buy(self, product):
        original_quantity = product.quantity
        product.buy(100)
        assert product.quantity == original_quantity - 100

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(1500)


class TestCart:
    def test_add_product(self, cart, product):
        cart.add_product(product, 7)
        assert product in cart.products
        assert cart.products[product] == 7

    def test_remove_product(self, cart, product):
        cart.add_product(product, 6)
        cart.remove_product(product, 3)
        assert cart.products[product] == 3

    def test_remove_product_completely(self, cart, product):
        cart.add_product(product, 2)
        cart.remove_product(product)
        assert product not in cart.products

    def test_clear_cart(self, cart, product):
        cart.add_product(product, 9)
        cart.clear()
        assert not cart.products

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 7)
        expected_total = 7 * product.price
        assert cart.get_total_price() == expected_total

    def test_buy_success(self, cart, product):
        cart.add_product(product, 123)
        cart.buy()
        assert product.quantity == 877

    def test_buy_error(self, cart):
        not_enough_stock = Product("limited edition", 1000, "rare item", 1)
        cart.add_product(not_enough_stock, 2)
        with pytest.raises(ValueError):
            cart.buy()
